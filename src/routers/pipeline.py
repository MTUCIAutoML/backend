import cv2
from typing import Optional

from fastapi import APIRouter, status, Depends
from fastapi.responses import StreamingResponse

from schemas.pipeline import TestConnection, StartingCam, ActionResponse
from schemas.pv_interface import Action
from db import get_database, Session
from broker.kafka import kafkaManager, ActionError
import errors

router = APIRouter()

def cs_processing(*args, cs, source, action):
    try:
        kafkaManager.action(cs.location, cs.login, cs.password, source, action)
        resp = ActionResponse(source_id=source, status=True)
    except ActionError as er:
        resp = ActionResponse(source_id=source, status=False, message=str(er))
    return resp



def gen(camera):
    video = cv2.VideoCapture()
    video.open(camera)
    print("streaming live feed of ", camera)
    while True:
        success, frame = video.read()
        if not success:
            break
        else:
            print('here')
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            print(frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@router.post('/test_connection', status_code=204)
def test_connection(params: TestConnection):
    return StreamingResponse(gen(params.source), media_type="multipart/x-mixed-replace;boundary=frame")


@router.post('/start')
def start_cam(
    cam_info: StartingCam,
    db: Session = Depends(get_database),
):
    resp = cs_processing(cs=cam_info, source='source', action=Action.START)



@router.post('/stop')
def start_cam(
    cam_info: StartingCam,
    db: Session = Depends(get_database),
):
    try:
        resp = cs_processing(cs=cam_info, source='source', action=Action.STOP)
    except Exception as err:
        print(err)
