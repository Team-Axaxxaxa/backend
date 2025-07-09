from sqlalchemy import func
from sqlalchemy.orm import Session

from src.models import TestTaker, Answer, Question


def get_answers_count(test_taker: TestTaker, session: Session):
    answer_count = (session.query(func.count())
                    .select_from(Answer)
                    .where(Answer.test_taker == test_taker.id)
                    .scalar())
    return answer_count

def get_questions_count(test_taker: TestTaker, session: Session):
    questions_count = session.query(Question).where(Question.for_male == test_taker.is_male).count()
    return questions_count
