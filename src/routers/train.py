import os.path as p
import time
from typing import List


from fastapi import APIRouter, Depends, Cookie, status, Response
from fastapi.responses import RedirectResponse

from starlette.responses import JSONResponse

from db import get_database, Session
from schemas.train import TrainingConf, TrainingConfGetFull
from s3.s3 import s3
from cvat.cvat import cvat_export_dataset
from models.user import TrainingConfiguration
from mlcore.celery_app import train
from auth import get_user
import errors

router = APIRouter()


@router.get('/all', response_model=List[TrainingConfGetFull])
async def get_all_configurations(db: Session = Depends(get_database),
                                 user=Depends(get_user)
                                 ):
    if user is None:
        raise errors.unauthorized()
    conf = db.query(TrainingConfiguration).all()
    return conf


@router.get('/{conf_id}', response_model=TrainingConfGetFull)
async def get_conf_by_id(conf_id: int,
                         db: Session = Depends(get_database),
                         user=Depends(get_user)
                         ):
    if user is None:
        raise errors.unauthorized()
    conf = db.query(TrainingConfiguration).filter_by(id=conf_id).first()
    return conf


@router.post('/')
async def create_configuration(params: TrainingConf,
                               db: Session = Depends(get_database),
                               user=Depends(get_user),
                               sessionid: str = Cookie(None), 
                               csrftoken: str = Cookie(None)
                               ):
    if user is None:
        raise errors.unauthorized()
    print(params)
    training_params = {
        'epochs': params.epochs,
        'time': params.time,
        'patience': params.patience,
        'batch': params.batch,
        'imgsz': params.imgsz,
        'optimizer': params.optimizer,
        'classes': params.class_names,
        'device': params.device,
        'dataset_id': params.dataset_id
    }

    new_conf = TrainingConfiguration(
        name=params.name,
        model=params.model,
        training_conf=training_params,
        created_by = user.id
    )
    db.add(new_conf)
    db.commit()

    export_status = cvat_export_dataset(sessionid, csrftoken, params.dataset_id, new_conf.id)
    if export_status == 202:
        new_conf.dataset_s3_location = f"/{new_conf.id}-dataset-{params.dataset_id}.zip"
        db.commit()
        
        while not s3.has_file(new_conf.dataset_s3_location, f"user-{user.id}"):
            time.sleep(5)

        task = train.delay(new_conf.id, user.id)
        return JSONResponse({"task_id": task.id})
    else:
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    
    # task = train.delay(new_conf.id, user.id)

    # return JSONResponse({"task_id": task.id})


# @router.post('/{conf_id}/dataset', status_code=204)
# async def upload_dataset(conf_id: int,
#                          dataset: UploadFile = File(...),
#                          db: Session = Depends(get_database),
#                          user=Depends(get_user)
#                          ):
#     if user is None:
#         raise errors.unauthorized()
#     data = await dataset.read()
#     try:
#         training = db.query(TrainingConfiguration).filter_by(id=conf_id).first()
#         if training.dataset_s3_location is not None:
#             raise
#         with TemporaryDirectory(prefix='data') as tmp:
#             with open(p.join(tmp, dataset.filename), 'wb') as f:
#                 f.write(data)
#             with open(p.join(tmp, dataset.filename), 'rb') as f:
#                 path = f'/user/{conf_id}/dataset/{dataset.filename}'
#                 s3.upload_file(f, path)
#         training.dataset_s3_location = path
#         db.commit()
#     except Exception:
#         print('error')
#         raise


# @router.post('/{conf_id}/start')
# async def start_training(conf_id: int,
#                          db: Session = Depends(get_database),
#                          user=Depends(get_user)
#                          ):
#     if user is None:
#         raise errors.unauthorized()
#     conf = db.query(TrainingConfiguration).filter_by(id=conf_id).first()
#     if conf is None:
#         raise
    
#     return JSONResponse({"task_id": task.id})


@router.delete('/{conf_id}')
async def delete_conf(conf_id: int,
                      db: Session = Depends(get_database),
                      user = Depends(get_user)):
    if user is None:
        raise errors.unauthorized()
    conf = db.query(TrainingConfiguration).filter_by(id=conf_id).first()
    if conf is None:
        raise
    db.delete(conf)


@router.get('/{conf_id}/{file_type}', status_code=302, response_class=RedirectResponse)
async def get_file(conf_id: int,
                   file_type: str,
                   db: Session = Depends(get_database),
                   user = Depends(get_user)):
    if user is None:
        raise errors.unauthorized()
    conf = db.query(TrainingConfiguration).filter_by(id=conf_id).first()
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
