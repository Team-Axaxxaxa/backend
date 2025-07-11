from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import UUID4
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette import status

from src.db import get_session
from src.models import Result, UiAnalysis
from src.schemas.get_ui_analysis import UiAnalysisResponse
from src.utils.ai_analysis.ai_model_factory import AiModelFactory
from src.utils.ai_analysis.generate_content import generate_content

api_router = APIRouter(tags=["Test results"])


@api_router.get(
    "/ui_analysis/{result_id}",
    status_code=status.HTTP_200_OK,
    response_model=UiAnalysisResponse,
    responses= {
        status.HTTP_404_NOT_FOUND: {
            "description": "Не найден такой результат",
        }
    },
)
def get_ui_analysis(
    result_id: str = Path(...),
    session: Session = Depends(get_session),
):
    result_uuid = UUID4(result_id)
    result_query = select(Result).where(Result.id == result_uuid)
    result = session.scalar(result_query)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Не найден такой результат",
        )

    ui_analysis_query = select(UiAnalysis).where(UiAnalysis.result == result_uuid)
    ui_analysis = session.scalar(ui_analysis_query)

    if ui_analysis:
        return UiAnalysisResponse(text=ui_analysis.text)

    content = generate_content(session, result_uuid)
    model = AiModelFactory.create()
    analysis = model.analyse(content)

    ui_analysis = UiAnalysis(result=result_uuid, text=analysis)
    session.add(ui_analysis)
    session.commit()

    return UiAnalysisResponse(text=analysis)
