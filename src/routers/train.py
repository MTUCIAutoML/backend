import os.path as p
from typing import List

from fastapi import APIRouter, UploadFile, File, Depends, BackgroundTasks
from fastapi.responses import RedirectResponse
from tempfile import TemporaryDirectory

from db import get_database, Session
from schemas.train import TrainingConf, TrainingConfGetFull
from s3.s3 import s3
from models.models import TrainingConfiguration
from mlcore.yolo import train_yolo
from auth import get_user

router = APIRouter()


@router.get('/all', response_model=List[TrainingConfGetFull])
async def get_all_configurations(db: Session = Depends(get_database),
                                 user=Depends(get_user)):
    conf = db.query(TrainingConfiguration).filter_by(created_by=user.id).all()
    return conf


@router.get('/{conf_id}', response_model=TrainingConfGetFull)
async def get_conf_by_id(conf_id: int,
                         db: Session = Depends(get_database),
                         user=Depends(get_user)):
    conf = db.query(TrainingConfiguration).filter_by(id=conf_id, created_by=user.id).first()
    return conf


@router.post('/', response_model=TrainingConfGetFull)
async def create_configuration(params: TrainingConf,
                               db: Session = Depends(get_database),
                               user=Depends(get_user)):
    print(params)
    training_params = {
        'epochs': params.epochs,
        'time': params.time,
        'patience': params.patience,
        'batch': params.batch,
        'imgsz': params.imgsz,
        'optimizer': params.optimizer,
        'classes': params.class_names,
        'device': params.device
    }

    new_conf = TrainingConfiguration(
        name=params.name,
        model=params.model,
        training_conf=training_params,
        created_by=user.id
    )
    db.add(new_conf)
    db.commit()

    return new_conf


@router.post('/{conf_id}/dataset', status_code=204)
async def upload_dataset(conf_id: int,
                         dataset: UploadFile = File(...),
                         db: Session = Depends(get_database),
                         user=Depends(get_user)):
    data = await dataset.read()
    try:
        training = db.query(TrainingConfiguration).filter_by(id=conf_id, created_by=user.id).first()
        if training.dataset_s3_location is not None:
            raise
        with TemporaryDirectory(prefix='data') as tmp:
            with open(p.join(tmp, dataset.filename), 'wb') as f:
                f.write(data)
            with open(p.join(tmp, dataset.filename), 'rb') as f:
                path = f'/user/{conf_id}/dataset/{dataset.filename}'
                s3.upload_file(f, path)
        training.dataset_s3_location = path
        db.commit()
    except Exception:
        print('error')
        raise


@router.post('/{conf_id}/start', status_code=204)
async def start_training(conf_id: int,
                         training: BackgroundTasks,
                         db: Session = Depends(get_database),
                         user=Depends(get_user)):
    conf = db.query(TrainingConfiguration).filter_by(id=conf_id, created_by=user.id).first()
    if conf is None:
        raise
    training.add_task(train_yolo, conf_id, db)


@router.delete('/{conf_id}')
async def delete_conf(conf_id: int,
                      db: Session = Depends(get_database),
                      user=Depends(get_user)):
    conf = db.query(TrainingConfiguration).filter_by(id=conf_id, created_by=user.id).first()
    if conf is None:
        raise
    db.delete(conf)


@router.get('/{conf_id}/{file_type}', status_code=302, response_class=RedirectResponse)
async def get_file(conf_id: int,
                   file_type: str,
                   db: Session = Depends(get_database),
                   user=Depends(get_user)):
    conf = db.query(TrainingConfiguration).filter_by(id=conf_id, created_by=user.id).first()
    if conf is None:
        raise
    if file_type == 'dataset':
        if conf.dataset_s3_location is None:
            raise
        return conf.s3_dataset_url
    elif file_type == 'pt':
        if conf.weight_s3_location is None:
            raise
        return conf.s3_weight_url
    elif file_type == 'onnx':
        return conf.s3_onnx_url
    else:
        raise
