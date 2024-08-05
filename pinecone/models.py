from pydantic import BaseModel


class QueryRequest(BaseModel):
    project_id: str
    query: str


class UploadRequest(BaseModel):
    project_name: str
    document: str
