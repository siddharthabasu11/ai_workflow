from app.core.celery_app import celery_app
from app.db.database import session_factory
from app.crud.repository import get_repository
from app.services.metrics import analyze_repository, get_code_sample
from app.services.ai_report import generate_report
from app.models.analysis import Analysis
from pathlib import Path
import shutil
import git


@celery_app.task
def clone_repository(repository_id: int):
    db = session_factory()
    try:
        repo = get_repository(db, repository_id)
        if repo is None:
            return

        repo.status = "cloning"
        db.commit()

        clone_path = Path(f"/tmp/atlas/repos/{repository_id}")
        if clone_path.exists():
            shutil.rmtree(clone_path)

        try:
            git.Repo.clone_from(repo.github_url, clone_path)
            repo.status = "cloned"
            db.commit()

            repo.status = "analyzing"
            db.commit()

            metrics = analyze_repository(clone_path)

            analysis = Analysis(
                repository_id=repo.id,
                file_count=metrics["file_count"],
                total_loc=metrics["total_loc"],
                language_breakdown=metrics["language_breakdown"],
                largest_files=metrics["largest_files"],
            )
            db.add(analysis)
            db.commit()

            repo.status = "analyzed"
            db.commit()

            repo.status = "generating_report"
            db.commit()

            code_sample = get_code_sample(clone_path)
            report_text = generate_report(metrics, code_sample)

            analysis.report = report_text
            db.commit()

            repo.status = "complete"
            db.commit()

        except Exception:
            repo.status = "failed"
            db.commit()
    finally:
        db.close()