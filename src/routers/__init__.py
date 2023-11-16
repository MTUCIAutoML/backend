from fastapi import APIRouter

from routers.model import router as model

router = APIRouter()

router.include_router(model, prefix='/model', tags=['Model'])
