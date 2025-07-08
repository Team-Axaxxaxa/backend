from pydantic import BaseModel


class QuestionCountResponse(BaseModel):
    count: int
