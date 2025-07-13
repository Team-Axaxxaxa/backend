import pytest
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from src.__main__ import app
from src.db import get_session
from src.models import Question
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
