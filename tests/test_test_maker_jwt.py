import uuid

import pytest
from fastapi import HTTPException
from jose import jwt
from sqlalchemy.orm import Session

from src.utils.settings import get_settings
from src.utils.test_maker_jwt import create_access_token, get_test_taker


@pytest.mark.parametrize(
    "test_taker_id",
    [
        "test_taker_id_1",
    ],
)
def test_create_access_token_ok(test_taker_id: str):
    encoded = create_access_token(test_taker_id)
    decoded = jwt.decode(encoded, get_settings().SECRET_KEY)
    assert decoded["id"] == test_taker_id


def test_get_test_taker_ok(test_taker: str, session: Session):
    test_taker_response = get_test_taker(test_taker, session)

    assert test_taker_response.is_male == True


def test_get_test_taker_not_found(session: Session):
    random_id = str(uuid.uuid4())
    test_taker = create_access_token(random_id)

    with pytest.raises(HTTPException):
        get_test_taker(test_taker, session)
