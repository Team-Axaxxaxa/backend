from pydantic import BaseModel, UUID4


class QuestionResponse(BaseModel):
    id: UUID4
    text: str
    for_male: bool
