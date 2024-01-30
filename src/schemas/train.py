from typing import Dict, Any, Optional, List
from datetime import datetime

from schemas.base import BaseModel


class TrainingConf(BaseModel):
    name: str
    model: str
    epochs: int
    time: Optional[int] = None
    patience: Optional[int] = 50
    batch: Optional[int] = 16
    imgsz: Optional[int] = 640
    optimizer: Optional[str] = 'auto'
    class_names: List[str]


class TrainingConfGetFull(BaseModel):
    id: int
    name: str
    model: str
    status: str
    s3_dataset_url: Optional[str]
    s3_weight_url: Optional[str]
    created_at: datetime
    training_conf: Dict[str, Any]


