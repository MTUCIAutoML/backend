from datetime import datetime

from schemas.base import BaseModel


class Model(BaseModel):
    id: int
    status_learning: str
    dataset_s3_path: str
    upload_date: datetime
    model: str
    weights_s3_path: str
