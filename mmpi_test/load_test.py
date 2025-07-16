from pathlib import Path
from typing import List, Dict

import pandas as pd
from dotenv import load_dotenv

from src.db import get_session, session_scope
from src.models import Question, Category, QuestionInCategory
from src.models.option_enum import OptionEnum

file = 'test.xlsx'

unusual_categories = [
        'Женские вопросы',
        'Мужские вопросы',
        'Лист-221',
        'Пустой лист/разграничитель',
        'А также/разделитель',
]

male_categories = [
    '«5-М» Женственность',
    '176. Rg-m. (Ригидность мужская)',
]

female_categories = [
    '«5-Ж» Женственность',
    '66. Fe. (Женственность). Gough,',
    '68. Fm. (Женский мазохизм).',
    '175. Rg-f. (Ригидность женская)',
    'Fem. (Женские интересы).'
]


def get_questions(df: pd.DataFrame) -> List[str]:
    return list(df.iloc[:, 0].dropna())


def get_answers(df: pd.DataFrame, line: int) -> List[int]:
    if line >= len(df):
        return []
    result = []
    for x in df.iloc[line].dropna():
        try:
            result.append(int(x))
        except ValueError:
            pass
    return result


def create_questions(session, questions: List[str], for_male: bool) -> List[Question]:
    question_models = []
    for question in questions:
        question_model = Question(text=question, for_male=for_male)
        session.add(question_model)
        question_models.append(question_model)
    session.commit()
    return question_models


def create_categories(session, categories: List[str]) -> Dict[str, Category]:
    category_models = {}
    for category in categories:
        category_model = Category(name=category)
        session.add(category_model)
        category_models[category] = category_model
    session.commit()
    return category_models


def main():
    with session_scope() as session:
        print('Сессия создана')

        excel_file = pd.ExcelFile(file)
        print('Файл прочитан')

        category_names = excel_file.sheet_names
        for category in unusual_categories + male_categories + female_categories:
            if category in category_names:
                category_names.remove(category)

        male_questions = get_questions(excel_file.parse('Мужские вопросы', header=None))
        female_questions = get_questions(excel_file.parse('Женские вопросы', header=None))

        print('Начато создание категорий')
        categories_dict = create_categories(session, category_names + male_categories + female_categories)

        print('Начато создание вопросов')
        male_question_models = create_questions(session, male_questions, True)
        female_question_models = create_questions(session, female_questions, False)

        added = 0
        print(f'Начата обработка общих категорий, всего категорий: {len(category_names)}')
        for order, category in enumerate(category_names):
            category_model = categories_dict[category]
            category_df = excel_file.parse(category, header=None)
            positive_answers = get_answers(category_df, 0)
            negative_answers = get_answers(category_df, 1)

            added_now = 0
            for answers, option in zip([positive_answers, negative_answers], [OptionEnum.YES, OptionEnum.NO]):
                for answer in answers:
                    question_index = int(answer) - 1
                    for question_model_list in [male_question_models, female_question_models]:
                        if question_index >= len(question_model_list):
                            continue
                        question_model = question_model_list[question_index]

                        question_in_category = QuestionInCategory(
                            category=category_model.id,
                            question=question_model.id,
                            increase_option = option,
                        )
                        session.add(question_in_category)
                        added_now += 1
            session.commit()

            added += added_now
            print(f'Обработана категория {category}, {order + 1}/{len(category_names)},'
                  f' добавлено {added_now} условий для категорий, всего добавлено {added} условий')

        print('Начата обработка мужских и женских категорий')
        for categories, question_model_list in zip(
            [male_categories, female_categories],
            [male_question_models, female_question_models],
        ):
            for category in categories:
                category_model = categories_dict[category]
                category_df = excel_file.parse(category, header=None)
                positive_answers = get_answers(category_df, 0)
                negative_answers = get_answers(category_df, 1)

                added_now = 0
                for answers, option in zip([positive_answers, negative_answers], [OptionEnum.YES, OptionEnum.NO]):
                    for answer in answers:
                        question_index = int(answer) - 1
                        if question_index >= len(question_model_list):
                            continue
                        question_model = question_model_list[question_index]

                        question_in_category = QuestionInCategory(
                            category=category_model.id,
                            question=question_model.id,
                            increase_option=option,
                        )
                        session.add(question_in_category)
                        added_now += 1
                session.commit()

                added += added_now
                print(f'Обработана категория {category},'
                      f' добавлено {added_now} условий для категорий, всего добавлено {added} условий')

if __name__ == '__main__':
    root_dir = Path(__file__).resolve().parent.parent
    load_dotenv(root_dir / '.env')

    main()
