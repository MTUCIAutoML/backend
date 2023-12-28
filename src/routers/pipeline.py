import cv2

from fastapi import APIRouter, status

from schemas.pipeline import TestConnection
import errors

router = APIRouter()


@router.post('/test', status_code=204)
def test_connection(params: TestConnection):
    print(params)
    cap = cv2.VideoCapture(params.source)
    if not cap.read()[0]:
        raise errors.RTSP_not_found()
