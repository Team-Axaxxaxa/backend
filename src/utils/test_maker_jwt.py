import re
from typing import Annotated

from jose import jwt, JWTError, ExpiredSignatureError
from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from datetime import datetime, timezone, timedelta

from pydantic import UUID4
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette import status

from src.db import get_session
from src.models import TestTaker
from src.utils.settings import get_settings


def create_access_token(id: str) -> str:
    to_encode = {'id': id}
    duration = get_settings().TEST_TOKEN_DURATION_MINUTES
    expire = datetime.now(timezone.utc) + timedelta(days=duration)
    to_encode.update({"exp": expire})
    settings = get_settings()
    encode_jwt = jwt.encode(to_encode, settings.SECRET_KEY)
    return encode_jwt


security = HTTPBearer()


def get_token(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]):
    return credentials.credentials


def get_test_taker(token: str = Depends(get_token), session: Session = Depends(get_session)) -> TestTaker:
    try:
        settings = get_settings()
        payload = jwt.decode(token, settings.SECRET_KEY)
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Токен истек')
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Токен не валидный!')

    test_taker_id = payload.get('id')
    if not test_taker_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Не найден ID пользователя')

    uuid_ = UUID4(test_taker_id)
    test_taker_query = select(TestTaker).where(TestTaker.id == uuid_)
    test_taker = session.scalar(test_taker_query)
    if not test_taker:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Пользователь не найден')

    return test_taker
