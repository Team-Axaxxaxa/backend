from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import UUID4
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette import status

from src.db import get_session
from src.models import Question
from src.schemas.question import QuestionResponse

api_router = APIRouter(tags=["Test taking"])


@api_router.get(
    "/question/by_id/{id}",
    status_code=status.HTTP_200_OK,
    response_model=QuestionResponse,
    responses= {
        status.HTTP_404_NOT_FOUND: {
            "description": "Не найден такой вопрос",
        }
    },
)
def get_question(
    id: str = Path(...),
    session: Session = Depends(get_session),
):
    uuid = UUID4(id)
    question_query = select(Question).where(Question.id == uuid)
    question = session.scalar(question_query)

    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Не найден такой вопрос",
        )

    return QuestionResponse(
        id=question.id,
        text=question.text,
        for_male=question.for_male,
    )
