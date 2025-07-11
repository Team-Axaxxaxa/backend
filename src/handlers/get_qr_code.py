from fastapi import APIRouter, Path
from starlette import status
from fastapi.responses import RedirectResponse

from src.utils.qr_code.qr_code_supplier_factory import QrCodeSupplierFactory

api_router = APIRouter(tags=["Test results"])


@api_router.get(
    "/qr_code/{url}",
    status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    response_class=RedirectResponse,
)
def get_question(
    url: str = Path(...),
):
    qr_code_supplier = QrCodeSupplierFactory.create()
    redirect_url = qr_code_supplier.generate_qr_code_link(url)

    return RedirectResponse(redirect_url)
