from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_engine(
    settings.database_url,
    echo = True
)

session_factory = sessionmaker(
    bind = engine,
    autoflush=False,
    autocommit= False
)

def get_db():
    db = session_factory()
    try:
        yield db
    finally:
        db.close()