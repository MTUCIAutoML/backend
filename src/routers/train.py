import os.path as p
from typing import List

from fastapi import APIRouter, UploadFile, File, Depends, BackgroundTasks
from tempfile import TemporaryDirectory

from db import get_database, Session
from schemas.train import TrainingConf, TrainingConfGetFull
from s3.s3 import s3
from models.models import TrainingConfiguration
from mlcore.yolo import train_yolo

router = APIRouter()


@router.get('/', response_model=List[TrainingConfGetFull])
async def get_all_configurations(db: Session = Depends(get_database)):
    conf = db.query(TrainingConfiguration).all()
    return conf


@router.get('/{conf_id}', response_model=TrainingConfGetFull)
async def get_conf_by_id(conf_id: int,
                         db: Session = Depends(get_database)):
    conf = db.query(TrainingConfiguration).filter_by(id=conf_id).first()
    return conf


@router.post('/', response_model=TrainingConfGetFull)
async def create_configuration(params: TrainingConf,
                               db: Session = Depends(get_database)):
    print(params)
    training_params = {
        'epochs': params.epochs,
        'time': params.time,
        'patience': params.patience,
        'batch': params.batch,
        'imgsz': params.imgsz,
        'optimizer': params.optimizer
    }

    new_conf = TrainingConfiguration(
        name=params.name,
        model=params.model,
        training_conf=training_params
    )
    db.add(new_conf)
    db.commit()

    return new_conf


@router.post('/{conf_id}/dataset', status_code=204)
async def upload_dataset(conf_id: int,
                         dataset: UploadFile = File(...),
                         db: Session = Depends(get_database)):
    data = await dataset.read()
    try:
        with TemporaryDirectory(prefix='data') as tmp:
            with open(p.join(tmp, dataset.filename), 'wb') as f:
                f.write(data)
            with open(p.join(tmp, dataset.filename), 'rb') as f:
                path = f'/user/{conf_id}/dataset/{dataset.filename}'
                s3.upload_file(f, path)
        training = db.query(TrainingConfiguration).filter_by(id=conf_id).first()
        training.dataset_s3_url = path
        db.commit()
    except Exception:
        print('error')
        raise


@router.post('/{conf_id}/start', status_code=204)
async def start_training(conf_id: int,
                         training: BackgroundTasks,
                         db: Session = Depends(get_database)):
    conf = db.query(TrainingConfiguration).filter_by(id=conf_id).first()
    if conf is None:
        raise
    training.add_task(train_yolo, conf_id, db)


@router.delete('/{conf_id}')
async def delete_conf(conf_id: int):
    pass