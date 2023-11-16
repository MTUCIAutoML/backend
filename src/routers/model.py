from typing import List

from fastapi import APIRouter, Depends

from db import get_database, Session
from models import models as m
from schemas.model import Model

router = APIRouter()


@router.get("/", response_model=List[Model])
async def get_all_learning_story(db: Session = Depends(get_database)):
    story = db.query(m.Model).all()
    return story if story is not None else []
