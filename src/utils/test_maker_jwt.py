import re

from jose import jwt, JWTError
from fastapi import Request, HTTPException, Depends
from datetime import datetime, timezone, timedelta

from pydantic import UUID4
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette import status

from src.db import get_session
from src.models import TestTaker
from src.utils.settings import get_settings

DURATION = 30

def create_access_token(id: str) -> str:
    to_encode = {'id': id}
    expire = datetime.now(timezone.utc) + timedelta(days=DURATION)
    to_encode.update({"exp": expire})
    settings = get_settings()
    encode_jwt = jwt.encode(to_encode, settings.SECRET_KEY)
    return encode_jwt


def get_token(request: Request):
    authorization = request.headers.get('Authorization')
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token not found')
    found = re.search('^Bearer \S+$', authorization)
    group = found.groups()[0]
    if not group:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Токен не корректный')
    return authorization


def get_test_taker(token: str = Depends(get_token), session: Session = Depends(get_session)):
    try:
        settings = get_settings()
        payload = jwt.decode(token, settings.SECRET_KEY)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Токен не валидный!')

    expire = payload.get('exp')
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Токен истек')

    test_taker_id = payload.get('id')
    if not test_taker_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Не найден ID пользователя')

    uuid_ = UUID4(test_taker_id)
    test_taker_query = select(TestTaker).where(TestTaker.id == uuid_)
    test_taker = session.scalar(test_taker_query)
    if not test_taker:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Пользователь не найден')

    return test_taker
