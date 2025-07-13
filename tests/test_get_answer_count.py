from fastapi.testclient import TestClient

from src.models import Answer
from src.utils.settings import get_settings


def test_get_answer_count_zero(test_taker: str, client: TestClient):
    settings = get_settings()
    response = client.get(
        f'{settings.PATH_PREFIX}/answer/count',
        headers={'Authorization': f'Bearer {test_taker}'}
    )
    assert response.status_code == 200
    assert response.json()['count'] == 0


def test_get_answer_count_one(test_taker: str, answer: Answer, client: TestClient):
    settings = get_settings()
    response = client.get(
        f'{settings.PATH_PREFIX}/answer/count',
        headers={'Authorization': f'Bearer {test_taker}'}
    )
    assert response.status_code == 200
    assert response.json()['count'] == 1
