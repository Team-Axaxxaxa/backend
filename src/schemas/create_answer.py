from pydantic import BaseModel, UUID4

from src.models.answer import OptionEnum


class CreateAnswerResponse(BaseModel):
    id: UUID4
    test_taker: UUID4
    question: UUID4
    option: OptionEnum


class CreateAnswerRequest(BaseModel):
    question: UUID4
    option: OptionEnum