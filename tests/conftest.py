import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient

from src.__main__ import app
from src.db import get_session
from src.models import Question, Answer
from src.models.option_enum import OptionEnum
from src.utils.settings import get_settings


@pytest.fixture
def session():
    yield get_session()


@pytest.fixture
def client():
    yield TestClient(app)


@pytest.fixture
def test_taker(client: TestClient, session: Session):
    settings = get_settings()
    response = client.post(settings.PATH_PREFIX + '/test_taker', json={'is_male': True})
    yield response.json()['access_token']


@pytest.fixture
def question(session: Session):
    question = Question(text='Simple question', for_male=True)
    session.add(question)
    session.commit()
    yield question
    session.delete(question)
    session.commit()


@pytest.fixture
def answer(question: Question, test_taker: str, client: TestClient, session: Session):
    settings = get_settings()
    response = client.post(
        f'{settings.PATH_PREFIX}/answer',
        json={'question': str(question.id), 'option': OptionEnum.YES.value},
        headers={'Authorization': f'Bearer {test_taker}'}
    )

    assert response.status_code == 200

    answer_id = response.json()['id']
    session.commit()
    answer_query = select(Answer).where(Answer.id == answer_id)
    answer = session.scalar(answer_query)
    yield answer

    session.delete(answer)
    session.commit()
