from typing import Iterable

from pydantic import UUID4
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from src.models import CategoryResult, Category, QuestionInCategory


def generate_content(session: Session, result_id: UUID4) -> str:
    content = ''
    with open('./src/utils/ai_analysis/default_message.txt', 'r') as f:
        content += f.read()
    content += generate_result_text(session, result_id)
    return content


def generate_result_text(session: Session, result_id: UUID4) -> str:
    category_result_models_query = select(CategoryResult).where(CategoryResult.result == result_id)
    category_result_models: Iterable[CategoryResult] = session.scalars(category_result_models_query).all()

    result_text = ''
    for category_result in category_result_models:
        category_query = select(Category).where(Category.id == category_result.category)
        category: Category = session.scalar(category_query)

        max_in_category = (session.query(func.count())
                        .select_from(QuestionInCategory)
                        .where(QuestionInCategory.category == category.id)
                        .scalar())

        result_text += (f'Для категории {category.name} итоговый результат {category_result.score}'
                        f' при этом максимум {max_in_category}\n')

    return result_text
