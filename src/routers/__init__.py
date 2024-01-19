from fastapi import APIRouter

from routers.pipeline import router as pipeline
from routers.train import router as train

router = APIRouter()

router.include_router(pipeline, prefix='/pipeline', tags=['Pipeline'])
router.include_router(train, prefix='/train', tags=['Train'])
