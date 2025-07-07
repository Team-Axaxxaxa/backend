from pydantic import BaseModel


class CreateTestTakerRequest(BaseModel):
    is_male: bool

class CreateTestTakerResponse(BaseModel):
    access_token: str
