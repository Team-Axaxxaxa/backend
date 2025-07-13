import pytest
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient

from src.models import Question
from src.utils.settings import get_settings


@pytest.mark.parametrize(
    'question_count',
    [
        pytest.param(0, id='zero'),
        pytest.param(1, id='one'),
        pytest.param(5, id='five'),
    ],
)
def test_get_question_count_default(question_count: int, test_taker: str,  client: TestClient, session: Session):
    questions = []
    for i in range(question_count):
        question = Question(text=f'Question {i}', for_male=True)
        questions.append(question)
    session.add_all(questions)
    session.commit()

    settings = get_settings()
    response = client.get(
        f'{settings.PATH_PREFIX}/question/count',
        headers={'Authorization': f'Bearer {test_taker}'}
    )
    assert response.status_code == 200

    count = response.json()['count']
    assert count == question_count

    for question_ in questions:
        session.delete(question_)
    session.commit()
