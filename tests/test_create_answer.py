import uuid

from fastapi.testclient import TestClient
from sqlalchemy import delete
from sqlalchemy.orm import Session

from src.models import Question, Answer
from src.models.option_enum import OptionEnum
from src.utils.settings import get_settings


def delete_answer(answer_id: str, session: Session):
    answer_query = delete(Answer).where(Answer.id == answer_id)
    session.execute(answer_query)
    session.commit()


def test_create_answer_ok(question: Question, test_taker: str, client: TestClient, session: Session):
    settings = get_settings()
    response = client.post(
        f'{settings.PATH_PREFIX}/answer',
        json={'question': str(question.id), 'option': OptionEnum.YES.value},
        headers={'Authorization': f'Bearer {test_taker}'}
    )
    assert response.status_code == 200

    session.commit()
    delete_answer(response.json()['id'], session)


def test_create_answer_no_question_found(test_taker: str, client: TestClient):
    settings = get_settings()
    response = client.post(
        f'{settings.PATH_PREFIX}/answer',
        json={'question': str(uuid.uuid4()), 'option': OptionEnum.YES.value},
        headers={'Authorization': f'Bearer {test_taker}'}
    )
    assert response.status_code == 404
