from fastapi import APIRouter, Depends, Body, HTTPException
from sqlalchemy import select, and_
from sqlalchemy.orm import Session
from starlette import status

from src.db import get_session
from src.models import TestTaker, Answer, Question
from src.schemas.create_answer import CreateAnswerResponse, CreateAnswerRequest
from src.utils.test_maker_jwt import get_test_taker

api_router = APIRouter(tags=["Test taking"])

@api_router.post(
    "/answer",
    status_code=status.HTTP_200_OK,
    response_model=CreateAnswerResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Не найден такой вопрос",
        }
    },
)
def create_answer(
    model: CreateAnswerRequest = Body(...),
    test_taker: TestTaker = Depends(get_test_taker),
    session: Session = Depends(get_session),
):
    question_query = select(Question).where(Question.id == model.id)
    question = session.scalar(question_query)

    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Не найден такой вопрос",
        )

    answer_query = select(Answer).where(
        and_(Answer.question == model.question, Answer.test_taker == test_taker.id)
    )
    answer: Answer = session.scalar(answer_query)

    if answer:
        answer.option = model.option
    else:
        answer = Answer(question=model.question, option=model.option, test_taker=test_taker.id)
        session.add(answer)
    session.commit()