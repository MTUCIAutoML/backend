from datetime import datetime
from typing import List

from sqlalchemy import func, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column
from models.base import Base, apply_status


class Model(Base):
    __tablename__ = "learned_models"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    status_learning: Mapped[str] = mapped_column(apply_status, nullable=False, index=True,
                                                 server_default='pending')
    dataset_s3_path: Mapped[str] = mapped_column(nullable=False)
    upload_date: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False,
                                                  server_default=func.current_timestamp())
    model: Mapped[str] = mapped_column(nullable=True)
    weights_s3_path: Mapped[str] = mapped_column(nullable=True)
