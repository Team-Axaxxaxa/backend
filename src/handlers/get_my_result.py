from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette import status

from src.db import get_session
from src.models import TestTaker, Result
from src.schemas.result import ResultResponse
from src.utils.test_maker_jwt import get_test_taker

api_router = APIRouter(tags=["Url"])


@api_router.get(
    "/result",
    status_code=status.HTTP_200_OK,
    response_model=ResultResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "У текущего пользователя нет результата",
        }
    },
)
def get_result(
    test_taker: TestTaker = Depends(get_test_taker),
    session: Session = Depends(get_session),
):
    if not test_taker.result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="У текущего пользователя нет результата",
        )

    result_query = select(Result).where(Result.id == test_taker.result)
    result = session.scalar(result_query)

    if not result:
        test_taker.result = None
        session.commit()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="У текущего пользователя нет результата",
        )

    return ResultResponse(id=result.id)
