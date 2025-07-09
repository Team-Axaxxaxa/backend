from pydantic import BaseModel

from src.models.answer import OptionEnum


class GetAnswerResponse(BaseModel):
    option: OptionEnum
