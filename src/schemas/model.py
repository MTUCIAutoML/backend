from datetime import datetime
from typing import Dict, Any

from schemas.base import BaseModel


class Model(BaseModel):
    id: int
    status_learning: str
    learning_params: Dict[str, Any]
    dataset_s3_path: str
    upload_date: datetime
    weights_s3_path: str
