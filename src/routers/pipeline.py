import cv2

from fastapi import APIRouter, status
from fastapi.responses import StreamingResponse

from schemas.pipeline import TestConnection
import errors

router = APIRouter()


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
