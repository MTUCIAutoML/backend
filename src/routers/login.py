import asyncio
import random

from fastapi import APIRouter, Depends, Cookie, Response, Body, status
from sqlalchemy.orm import undefer_group

import errors
from auth import get_user, init_tokens, refresh_tokens
from db import Session, get_database
from models.user import User
from schemas.login import Refresh, AccountCredentials, UserResponse
from cvat.cvat import cvat_register_user, cvat_login_user, cvat_s3_create
from s3.s3 import s3

router = APIRouter()


@router.post('', response_model=Refresh)
async def login(
    response: Response,
    credentials: AccountCredentials,
    db: Session = Depends(get_database)
):
    user = db.query(User).options(undefer_group("sensitive")).filter_by(email=credentials.login).first()
    await asyncio.sleep(random.random())
    if user is None:
        raise errors.invalid_credentials()
    if not user.verify_password(credentials.password):
        raise errors.invalid_credentials()
    cookie = cvat_login_user(credentials.password, credentials.login)
    response.set_cookie('sessionid', cookie['sessionid'])
    response.set_cookie('csrftoken', cookie['csrftoken'])
    return init_tokens(user, response)


@router.post('/refresh', response_model=Refresh)
async def refresh_token(
    response: Response,
    access: str = Cookie(None),
    params: Refresh = Body(),
    db: Session = Depends(get_database)
):
    return refresh_tokens(access, params.refresh, response, db)


@router.delete('', status_code=status.HTTP_204_NO_CONTENT)
async def logout(response: Response):
    response.delete_cookie(key='access')


@router.post('/register', response_model=UserResponse)
async def register_user(
    credentials: AccountCredentials,
    db: Session = Depends(get_database)
):
    user = db.query(User).options(undefer_group("sensitive")).filter_by(email=credentials.login).first()
    if user is not None:
        raise errors.unable_to_create_account()
    user = User()
    user.email = credentials.login
    user.password = credentials.password
    db.add(user)
    db.commit()
    
    cvat_register_user(credentials.login, credentials.password, credentials.login)
    s3.create_bucket(f"user-{user.id}")
    cookie = cvat_login_user(credentials.password, credentials.login)
    print(cookie)
    cvat_s3_create(cookie['sessionid'], cookie['csrftoken'], user.id)
    return UserResponse.from_orm(user)

    