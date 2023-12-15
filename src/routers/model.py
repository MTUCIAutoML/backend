from typing import List, Optional

from fastapi import APIRouter, Depends, status, BackgroundTasks, UploadFile

import errors
from db import get_database, Session
from models.models import ModelHistory
from schemas.model import ModelHistoryGet, TrainCreate
from routers.training_utils import train_yolo

router = APIRouter()


@router.get("/all", response_model=List[ModelHistoryGet])
async def get_all_learning_story(db: Session = Depends(get_database)):
    story = db.query(ModelHistory).all()
    return story if story is not None else []


@router.get("/{training_id}", response_model=ModelHistoryGet)
async def get_training_by_id(training_id: int,
                             db: Session = Depends(get_database)):
    model = db.query(ModelHistory).filter_by(id=training_id).first()
    if model is None:
        raise
    return model


@router.post("/", response_model=ModelHistoryGet)
async def init_training(background_tasks: BackgroundTasks,
                        params: TrainCreate,
                        db: Session = Depends(get_database)):
    training = ModelHistory(
        learning_params=params.dict(),
        dataset_s3_path='',
    )
    db.add(training)
    db.commit()
    background_tasks.add_task(train_yolo, training.id, db)
    return training


@router.delete("/{training_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_training(training_id: int,
                          db: Session = Depends(get_database)):
    model = db.query(ModelHistory).filter_by(id=training_id).first()

    if model is None:
        raise

    db.delete(model)
    db.commit()

