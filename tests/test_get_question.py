import uuid

from fastapi.testclient import TestClient

from src.models import Question
from src.utils.settings import get_settings


def test_get_question_ok(question: Question, client: TestClient):
    settings = get_settings()
    response = client.get(f'{settings.PATH_PREFIX}/question/by_id/{question.id}')
    assert response.status_code == 200
    assert response.json()['id'] == str(question.id)


def test_get_question_not_found(client: TestClient):
    question_id = str(uuid.uuid4())
    settings = get_settings()
    response = client.get(f'{settings.PATH_PREFIX}/question/by_id/{question_id}')
    assert response.status_code == 404
