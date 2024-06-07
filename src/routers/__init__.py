from fastapi import APIRouter

from routers.pipeline import router as pipeline
from routers.train import router as train
from routers.login import router as login
from routers.dataset import router as dataset
from routers.device import router as device

router = APIRouter()

router.include_router(pipeline, prefix='/pipeline', tags=['Pipeline'])
router.include_router(train, prefix='/train', tags=['Train'])
router.include_router(login, prefix='/user', tags=['Login'])
router.include_router(dataset, prefix='/dataset', tags=['Dataset'])
router.include_router(device, prefix='/device', tags=['Device'])
