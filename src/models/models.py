from datetime import datetime
from typing import Dict, Any

from sqlalchemy import func, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column
from models.base import Base, apply_status

from settings import settings
from s3.s3 import s3


class TrainingConfiguration(Base):
    __tablename__ = 'training_configurations'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    model: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(apply_status, nullable=False, index=True, server_default='pending')
    dataset_s3_location: Mapped[str] = mapped_column(nullable=True)
    weight_s3_location: Mapped[str] = mapped_column(nullable=True)
    onnx_s3_location: Mapped[str] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False,
                                                 server_default=func.current_timestamp())
    created_by: Mapped[int] = mapped_column(ForeignKey('user.id'), index=True)
    training_conf: Mapped[Dict[str, Any]] = mapped_column(JSONB, nullable=False)
    result_metrics: Mapped[Dict[str, Any]] = mapped_column(JSONB, nullable=True)
    '''
    epoch
    time
    patience
    batch
    imgsz
    optimizer
    '''

    @hybrid_property
    def s3_dataset_url(self):
        return s3.generate_link(bucket=settings.AWS_BUCKET, key=self.dataset_s3_location)

    @hybrid_property
    def s3_weight_url(self):
        return s3.generate_link(bucket=settings.AWS_BUCKET, key=self.weight_s3_location)
    
    @hybrid_property
    def s3_onnx_url(self):
        return s3.generate_link(bucket=settings.AWS_BUCKET, key=self.onnx_s3_location)


