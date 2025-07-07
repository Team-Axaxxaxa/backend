from pydantic import BaseModel, UUID4

from src.models.question import IncreaseOptionEnum


class RandomUnfilledQuestionResponse(BaseModel):
    id: UUID4
    category: UUID4
    text: str
    for_male: bool
    increase_option: IncreaseOptionEnum
