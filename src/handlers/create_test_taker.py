from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from starlette import status

from src.db import get_session
from src.models import TestTaker
from src.schemas.create_test_taker import CreateTestTakerResponse, CreateTestTakerRequest
from src.utils.test_maker_jwt import create_access_token

api_router = APIRouter(tags=["Url"])

@api_router.post(
    "/test_taker",
    status_code=status.HTTP_200_OK,
    response_model=CreateTestTakerResponse,
)
async def create_test_taker(
    model: CreateTestTakerRequest = Body(..., example={
        'is_male': True,
    }),
    session: Session = Depends(get_session),
):
    test_taker = TestTaker(is_male=model.is_male)
    session.add(test_taker)
    session.commit()

    access_token = create_access_token(str(test_taker.id))
    return CreateTestTakerResponse(access_token=access_token)
