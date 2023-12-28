from fastapi import APIRouter

from routers.model import router as model
from routers.pipeline import router as pipeline

router = APIRouter()

router.include_router(model, prefix='/model', tags=['Model'])
router.include_router(pipeline, prefix='/pipeline', tags=['Pipeline'])
