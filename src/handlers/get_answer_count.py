from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from src.db import get_session
from src.models import TestTaker
from src.schemas.get_answer_count import AnswerCountResponse
from src.utils.question_count import get_answers_count
from src.utils.test_maker_jwt import get_test_taker

api_router = APIRouter(tags=["Test taking"])


@api_router.get(
    "/answer/count",
    status_code=status.HTTP_200_OK,
    response_model=AnswerCountResponse,
)
def get_answer_count(
    test_taker: TestTaker = Depends(get_test_taker),
    session: Session = Depends(get_session),
):
    answer_count = get_answers_count(test_taker, session)

    return AnswerCountResponse(count=answer_count)
