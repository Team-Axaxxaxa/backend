from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from src.db import get_session
from src.models import TestTaker
from src.schemas.get_question_count import QuestionCountResponse
from src.utils.question_count import get_questions_count
from src.utils.test_maker_jwt import get_test_taker

api_router = APIRouter(tags=["Test taking"])


@api_router.get(
    "/question/count",
    status_code=status.HTTP_200_OK,
    response_model=QuestionCountResponse,
)
def get_question_count(
    test_taker: TestTaker = Depends(get_test_taker),
    session: Session = Depends(get_session),
):
    question_count = get_questions_count(test_taker, session)

    return QuestionCountResponse(count=question_count)
