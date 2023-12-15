from typing import List

from ultralytics import YOLO
from fastapi import Depends

from db import get_database, Session
from models.models import ModelHistory
from models.base import apply_status


async def train_yolo(training_id: int,
                     db: Session):
    #TODO generate yaml files and work with files
    model = db.query(ModelHistory).filter_by(id=training_id).first()
    yolo = YOLO('yolov8n.yaml')
    model.status_learning = 'processing'
    db.commit()
    results = yolo.train(data='coco128.yaml', epochs=model.learning_params['epochs'], device=0)
    model.status_learning = 'processed'
    db.commit()
