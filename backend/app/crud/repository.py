from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.repository import Repository

#needs all three because it no longer parses
def create_repository(db: Session, github_url: str, owner: str, name: str) -> Repository:
    db_repository = Repository(
        github_url = github_url,
        owner = owner,
        name = name,
    )
    db.add(db_repository)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ValueError(f"Repository with github_url '{github_url}' already exists")
    db.refresh(db_repository)
    return db_repository

def get_repository(db: Session, repository_id: int) -> Repository | None:
    return db.get(Repository, repository_id)

def get_repositories(db: Session, skip: int = 0, limit: int = 100)-> list[Repository]:
    return db.query(Repository).offset(skip).limit(limit).all()
