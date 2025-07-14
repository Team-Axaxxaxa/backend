import uuid

from fastapi.testclient import TestClient

from src.models import Answer
from src.utils.settings import get_settings


def test_get_answer_ok(answer: Answer, test_taker: str, client: TestClient):
    settings = get_settings()
    response = client.get(
        f'{settings.PATH_PREFIX}/answer/by_id/{str(answer.question)}',
        headers={'Authorization': f'Bearer {test_taker}'}
    )
    assert response.status_code == 200
    assert response.json()['option'] == answer.option.value


def test_get_answer_not_found(test_taker: str, client: TestClient):
    settings = get_settings()
    response = client.get(
        f'{settings.PATH_PREFIX}/answer/by_id/{str(uuid.uuid4())}',
        headers={'Authorization': f'Bearer {test_taker}'}
    )
    assert response.status_code == 404
