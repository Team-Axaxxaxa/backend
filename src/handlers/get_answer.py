from fastapi import APIRouter, Depends, Path, HTTPException
from pydantic import UUID4
from sqlalchemy import select, and_
from sqlalchemy.orm import Session
from starlette import status

from src.db import get_session
from src.models import TestTaker, Answer
from src.schemas.get_answer import GetAnswerResponse
from src.utils.test_maker_jwt import get_test_taker

api_router = APIRouter(tags=["Test taking"])


@api_router.get(
    "/answer/by_id/{question_id}",
    status_code=status.HTTP_200_OK,
    response_model=GetAnswerResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Не найден такой ответ",
        }
    },
)
def get_answer(
    question_id: str = Path(...),
    test_taker: TestTaker = Depends(get_test_taker),
    session: Session = Depends(get_session),
):
    question_uuid = UUID4(question_id)

    answer_query = select(Answer).where(
        and_(Answer.question == question_uuid, Answer.test_taker == test_taker.id)
    )
    answer = session.scalar(answer_query)

    if not answer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Не найден такой ответ",
        )

    return GetAnswerResponse(option=answer.option)
