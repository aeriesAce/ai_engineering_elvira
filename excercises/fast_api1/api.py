from fastapi import FastAPI, APIRouter
from .data_processing import Results

app = FastAPI()
router = APIRouter(prefix="/api/results")

@router.get("")
async def read_results():
    results = Results()
    return results.json_response()

@router.get("/schools")
async def filter_by_school(school: str):
    results = Results()
    return results.filter_school(school).json_response()

app.include_router(router)