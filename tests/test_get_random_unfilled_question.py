from fastapi.testclient import TestClient

from src.models import Question
from src.utils.settings import get_settings


def test_get_random_unfilled_question_ok(test_taker: str, question: Question, client: TestClient):
    settings = get_settings()
    response = client.get(
        settings.PATH_PREFIX + '/question/random',
        headers={'Authorization': f'Bearer {test_taker}'}
    )
    assert response.status_code == 200
    assert response.json()['text'] == question.text


def test_get_random_unfilled_question_not_found(test_taker: str, client: TestClient):
    settings = get_settings()
    response = client.get(
        settings.PATH_PREFIX + '/question/random',
        headers={'Authorization': f'Bearer {test_taker}'}
    )
    assert response.status_code == 404
