from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session
from starlette import status

from src.db import get_session
from src.schemas.get_category_results import CategoryResultsResponse
from src.utils.category_result import get_category_result_with_params

api_router = APIRouter(tags=['Test results'])


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
    result = get_category_result_with_params(None, result_id, session)
    return result


@api_router.get(
    '/category_results/main/{result_id}',
    status_code=status.HTTP_200_OK,
    response_model=CategoryResultsResponse,
    responses= {
        status.HTTP_404_NOT_FOUND: {
            'description': 'Не найден результат с таким id',
        }
    },
)
def get_category_result_main(
    result_id: str = Path(...),
    session: Session = Depends(get_session),
):
    result = get_category_result_with_params(True, result_id, session)
    return result


@api_router.get(
    '/category_results/other/{result_id}',
    status_code=status.HTTP_200_OK,
    response_model=CategoryResultsResponse,
    responses= {
        status.HTTP_404_NOT_FOUND: {
            'description': 'Не найден результат с таким id',
        }
    },
)
def get_category_result_other(
    result_id: str = Path(...),
    session: Session = Depends(get_session),
):
    result = get_category_result_with_params(False, result_id, session)
    return result
