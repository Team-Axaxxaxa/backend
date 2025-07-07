from pydantic import BaseModel, UUID4

from src.models.answer import OptionEnum


class AnswerResponse(BaseModel):
    id: UUID4
    test_taker: UUID4
    question: UUID4
    option: OptionEnum


class AnswerRequest(BaseModel):
    question: UUID4
    option: OptionEnum