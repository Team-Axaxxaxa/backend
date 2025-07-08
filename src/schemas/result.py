from pydantic import BaseModel, UUID4


class ResultResponse(BaseModel):
    id: UUID4
