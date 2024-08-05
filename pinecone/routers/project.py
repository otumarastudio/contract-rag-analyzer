from fastapi import APIRouter, HTTPException, UploadFile, File
from models import QueryRequest
from services.query_processor import QueryProcessor
from services.project_manager import ProjectManager

router = APIRouter()

query_processor = QueryProcessor()
project_manager = ProjectManager()


@router.post("/projects/{project_id}/query/basic")
async def query_basic_project(request: QueryRequest):
    try:
        response = await query_processor.basic_query(request.project_id, request.query)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/projects/{project_id}/query/enhanced")
async def query_enhanced_project(request: QueryRequest):
    try:
        response = await query_processor.query_with_enhancement(request.project_id, request.query)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/projects/{project_id}/query/split")
async def query_split_project(request: QueryRequest):
    try:
        response = await query_processor.query_with_split(request.project_id, request.query)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/projects/upload")
async def upload_project(project_name: str, file: UploadFile = File(...)):
    try:
        response = await project_manager.upload_project(project_name, file)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
