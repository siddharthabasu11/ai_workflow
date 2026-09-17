from datetime import datetime

from pydantic import BaseModel, ConfigDict

class RepositoryCreate(BaseModel):
    github_url : str

class RepositoryRead(BaseModel):
    id:int
    github_url:str
    owner:str
    name:str
    status:str
    created_at:datetime
    updated_at:datetime

    model_config = ConfigDict(from_attributes=True)
    