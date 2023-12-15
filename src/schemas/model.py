from datetime import datetime
from typing import Dict, Any, List, Optional

from schemas.base import BaseModel


class ModelHistoryGet(BaseModel):
    id: int
    status_learning: str
    learning_params: Dict[str, Any]
    dataset_s3_path: str
    upload_date: datetime
    weights_s3_path: Optional[str]


class TrainCreate(BaseModel):
    epochs: int
    class_names: List[str]
    