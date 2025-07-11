from pydantic import BaseModel


class UiAnalysisResponse(BaseModel):
    text: str
