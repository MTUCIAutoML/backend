import torch
import psutil

from fastapi import APIRouter

from schemas.device import Device

router = APIRouter()


@router.get("/gpu")
async def get_gpu_memory():
    if torch.cuda.is_available():
        free = torch.cuda.mem_get_info()[0] / 1024 ** 3
        total = torch.cuda.mem_get_info()[1] / 1024 ** 3
        return Device(
            total=str(total),
            usage=str(total - free)
        )
    raise


@router.get("/cpu")
async def get_cpu_usage():
    return Device(
        total=str(psutil.virtual_memory() [0] / 1024 ** 3),
        usage=str(psutil.virtual_memory() [3] / 1024 ** 3)
    )
