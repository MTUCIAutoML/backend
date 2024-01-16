from fastapi import APIRouter

from routers.pipeline import router as pipeline

router = APIRouter()

router.include_router(pipeline, prefix='/pipeline', tags=['Pipeline'])
