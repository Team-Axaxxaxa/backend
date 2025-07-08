from typing import Iterable

from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import UUID4
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette import status

from src.db import get_session
from src.models import Result, CategoryResult, Category
from src.schemas.get_category_results import CategoryResultsResponse

api_router = APIRouter(tags=['Test results'])


class BadCategory(Exception):
    pass


@api_router.get(
    '/category_results/{result_id}',
    status_code=status.HTTP_200_OK,
    response_model=CategoryResultsResponse,
    responses= {
        status.HTTP_404_NOT_FOUND: {
            'description': 'Не найден результат с таким id',
        }
    },
)
def get_category_result(
    result_id: str = Path(...),
    session: Session = Depends(get_session),
):
    result_uuid = UUID4(result_id)
    result_query = select(Result).where(Result.id == result_uuid)
    result = session.scalar(result_query)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Не найден результат с таким id'
        )

    category_result_models_query = select(CategoryResult).where(CategoryResult.result == result.id)
    category_result_models: Iterable[CategoryResult] = session.scalars(category_result_models_query).all()

    response_array = []
    for model in category_result_models:
        category_query = select(Category).where(Category.id == model.category)
        category: Category = session.scalar(category_query)

        if not category:
            raise BadCategory()

        category_result = CategoryResult(category_name=category.name, score=model.score)
        response_array.append(category_result)

    return CategoryResultsResponse(category_results=response_array)
