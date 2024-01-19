import os
import zipfile
import glob
import shutil

from ultralytics import YOLO
from tempfile import TemporaryDirectory

import os.path as p

from db import Session
from models.models import TrainingConfiguration
from s3.s3 import s3


async def train_yolo(conf_id: int,
                     db: Session):
    conf = db.query(TrainingConfiguration).filter_by(id=conf_id).first()
    yolo = YOLO(str(conf.model) + '.yaml')
    conf.status = 'processing'
    db.commit()
    with TemporaryDirectory(dir=os.getcwd()) as tmp:
        print(tmp)
        with open(tmp + f'{conf.name}.zip', mode='w+b') as f:
            print('Download')
            s3.download_file(f, conf.dataset_s3_url)
        with zipfile.ZipFile(tmp + f'{conf.name}.zip', 'r') as f:
            f.extractall(path=tmp + '/dataset')
            print('extract')
        with open(tmp + '/dataset/test.yaml', 'w') as f:
            f.writelines(['path: ' + tmp + '/dataset\n',
                          'train: train/images\n',
                          'val: val/images\n',
                          'names:\n',
                          '  0: person\n'])

        yolo.train(
            data=tmp + '/dataset/test.yaml',
            project=tmp,
            name=conf.name,
            epochs=conf.training_conf['epochs'],
            patience=conf.training_conf['patience'],
            batch=conf.training_conf['batch'],
            imgsz=conf.training_conf['imgsz'],
            optimizer=conf.training_conf['optimizer'],
            device='cpu'
        )
        print(glob.glob(tmp + '/*'))
        with zipfile.ZipFile(tmp + '/result.zip', 'w') as f:
            for dirname, subdirs, files in os.walk(tmp+f'/{conf.name}'):
                f.write(dirname)
                for filename in files:
                    f.write(p.join(dirname, filename))
        with open(tmp + '/result.zip', 'rb') as f:
            s3.upload_file(f, f'/automl/user/{conf_id}/result/result.zip')

    conf.status = 'processed'
    db.commit()
