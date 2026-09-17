from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from fastapi import HTTPException
from app.crud.repository import create_repository, get_repositories, get_repository
from app.db.database import get_db
from app.schemas.repository import RepositoryCreate,RepositoryRead
from app.utils.github import parse_github_url
from app.workers.task import clone_repository
from app.models.analysis import Analysis


router = APIRouter(prefix = "/repositories", tags = ["repositories"])

@router.post("/", response_model = RepositoryRead, status_code=201)
def submit_repository(repository:RepositoryCreate, db: Session = Depends(get_db)):
    try:
        owner, name = parse_github_url(repository.github_url)
    except ValueError as e:
        raise HTTPException(status_code=422, detail = str(e))
    
    normalized_url = f"https://github.com/{owner}/{name}"
    try:
        new_repo =  create_repository(db, normalized_url, owner, name)
        clone_repository.delay(new_repo.id)
        return new_repo
    except ValueError as e:
        raise HTTPException(status_code=409, detail = str(e))

@router.get("/{repository_id}", response_model=RepositoryRead)
def read_repository(repository_id: int, db: Session = Depends(get_db)):
    repository = get_repository(db, repository_id)
    if repository is None:
        raise HTTPException(status_code=404, detail = "Repository not found")
    return repository

@router.get("/", response_model=list[RepositoryRead])
def read_repositories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_repositories(db, skip, limit)


@router.get("/{repository_id}/analysis")
def get_analysis(repository_id: int, db: Session = Depends(get_db)):
    analysis = db.query(Analysis).filter(Analysis.repository_id == repository_id).first()
    if analysis is None:
        raise HTTPException(status_code=404, detail="Analysis not found for this repository")
    return {
        "repository_id": analysis.repository_id,
        "file_count": analysis.file_count,
        "total_loc": analysis.total_loc,
        "language_breakdown": analysis.language_breakdown,
        "largest_files": analysis.largest_files,
        "report": analysis.report,
    }