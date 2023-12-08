from typing import List

from fastapi import APIRouter, Depends, status

from db import get_database, Session
from models import models as m
from schemas.model import Model

router = APIRouter()


@router.get("/", response_model=List[Model])
async def get_all_learning_story(db: Session = Depends(get_database)):
    story = db.query(m.Model).all()
    return story if story is not None else []


@router.get("/{training_id}", response_model=Model)
async def get_training_by_id(training_id: int,
                             db: Session = Depends(get_database)):
    model = db.query(m.Model).filter_by(id=training_id).first()
    if model is None:
        raise
    return model


@router.post("/")
async def init_training(db: Session = Depends(get_database)):
    pass


@router.delete("/{training_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_trainig(training_id: int,
                         db: Session = Depends(get_database)):
    model = db.query(m.Model).filter_by(id=training_id).first()

    if model is None:
        raise

    db.delete(model)
    db.commit()

