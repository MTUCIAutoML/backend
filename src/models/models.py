from datetime import datetime
from typing import Dict, Any

from sqlalchemy import func, TIMESTAMP
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from models.base import Base, apply_status


class TrainingConfiguration(Base):
    __tablename__ = 'training_configurations'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    #TODO: do model enum
    model: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(apply_status, nullable=False, index=True, server_default='pending')
    dataset_s3_url: Mapped[str] = mapped_column(nullable=True)
    weight_s3_url: Mapped[str] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False,
                                                 server_default=func.current_timestamp())
    training_conf: Mapped[Dict[str, Any]] = mapped_column(JSONB, nullable=False)
    '''
    epoch
    time
    patience
    batch
    imgsz
    optimizer
    '''

