from fastapi import APIRouter
from starlette import status

api_router = APIRouter(tags=['Health'])

@api_router.get(
    '/health',
    status_code=status.HTTP_200_OK,
)
def get_health():
    return {'message': 'healthy!'}
