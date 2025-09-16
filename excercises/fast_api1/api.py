from fastapi import FastAPI, APIRouter, Query
from .data_processing import Results

app = FastAPI()
router = APIRouter(prefix="/api")

@router.get("")
async def read_results(limit: int = Query(100, gt=0)):
    results = Results(limit)
    return results.json_response()

@router.get("/results/schools")
async def filter_by_school(school: str):
    results = Results()
    return results.filter_school(school).json_response()

@router.get("/results/filter")
async def filter_by_fields(filter_:str):
    results = Results()
    return results.filter_fields(filter_).json_response()

@router.get("/results/approved")
async def appr():
    results = Results()
    return results.approved().json_response()

@router.get("/results/denied")
async def den():
    results = Results()
    return results.denied().json_response()

app.include_router(router)
