from typing import List

from pydantic import BaseModel


class CategoryResultModel(BaseModel):
    category_name: str
    score: int


class CategoryResultsResponse(BaseModel):
    category_results: List[CategoryResultModel]
