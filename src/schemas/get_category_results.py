from typing import List

from pydantic import BaseModel


class CategoryResult(BaseModel):
    category_name: str
    score: int


class CategoryResultsResponse(BaseModel):
    category_results: List[CategoryResult]
