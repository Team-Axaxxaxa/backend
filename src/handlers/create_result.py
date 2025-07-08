from typing import Iterable

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func, and_
from sqlalchemy.orm import Session
from sqlalchemy.sql.sqltypes import UUID
from starlette import status

from src.db import get_session
from src.models import TestTaker, Answer, Question, Result, CategoryResult
from src.models.question_in_category import QuestionInCategory
from src.schemas.result import ResultResponse
from src.utils.question_count import get_answers_count, get_questions_count
from src.utils.test_maker_jwt import get_test_taker

api_router = APIRouter(tags=["Test taking"])


@api_router.post(
    "/result",
    status_code=status.HTTP_200_OK,
    response_model=ResultResponse,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Не все вопросы были пройдены",
        }
    },
)
def create_result(
    test_taker: TestTaker = Depends(get_test_taker),
    session: Session = Depends(get_session),
):
    if test_taker.result:
        return ResultResponse(id=test_taker.result.id)

    answer_count = get_answers_count(test_taker, session)

    questions_count = get_questions_count(test_taker, session)

    if answer_count != questions_count:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Не все вопросы были пройдены",
        )

    result = Result()
    session.add(result)
    session.commit()

    try:
        count_category_results(result, test_taker, session)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Ошибка при создании результата'
        )

    test_taker.result = result.id
    session.commit()

    return ResultResponse(id=result.id)


def count_category_results(result: Result, test_taker: TestTaker, session: Session) -> None:
    answers_query = select(Answer).where(Answer.test_taker == test_taker.id)
    answers: Iterable[Answer] = session.scalars(answers_query).all()

    for answer in answers:
        question_in_category_query = select(QuestionInCategory).where(and_(
            QuestionInCategory.question == answer.question, QuestionInCategory.increase_option == answer.option
        ))

        questions_in_category: Iterable[QuestionInCategory] = session.scalars(question_in_category_query).all()

        for question_in_category in questions_in_category:
            category_result = get_or_create_category_result(result, question_in_category.category, session)
            category_result.score += 1
            session.commit()


def get_or_create_category_result(result: Result, category_id: UUID, session: Session) -> CategoryResult:
    category_result_query = select(CategoryResult).where(
        and_(CategoryResult.result == result.id, CategoryResult.category == category_id)
    )
    category_result = session.scalar(category_result_query)

    if category_result:
       return category_result

    category_result = CategoryResult(result=result.id, category=category_id, score=0)
    session.add(category_result)
    session.commit()

    return category_result
