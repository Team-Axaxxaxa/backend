from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, exists, and_
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import func
from starlette import status

from src.db import get_session
from src.models import TestTaker, Question, Answer
from src.schemas.question import QuestionResponse
from src.utils.test_maker_jwt import get_test_taker

api_router = APIRouter(tags=["Url"])

@api_router.get(
    "/question/random",
    status_code=status.HTTP_200_OK,
    response_model=QuestionResponse,
    responses= {
        status.HTTP_404_NOT_FOUND: {
            "description": "Нет не пройденных вопросов",
        }
    },
)
async def get_random_unfilled_question(
    test_taker: TestTaker = Depends(get_test_taker),
    session: Session = Depends(get_session),
):
    question_query = select(Question).where(
        ~exists().where(and_(Answer.question == Question.id, Answer.test_taker == test_taker.id))
    ).order_by(func.random())
    question = session.scalars(question_query).first()

    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Нет не пройденных вопросов",
        )

    return QuestionResponse(
        id=question.id,
        text=question.text,
        for_male=question.for_male,
    )
