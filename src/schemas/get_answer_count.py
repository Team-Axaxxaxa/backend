from pydantic import BaseModel


class AnswerCountResponse(BaseModel):
    count: int
