from fastapi import HTTPException, status


def with_errors(*errors: HTTPException):
    d = {}
    for err in errors:
        if err.status_code in d:
            d[err.status_code]["description"] += f"\n\n{err.detail}"
        else:
            d[err.status_code] = {"description": err.detail}
    return d


def learning_session_not_found():
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Learning session not found")


def RTSP_not_found():
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not Found')
