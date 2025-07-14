from fastapi import APIRouter, Path, Query
from starlette import status
from fastapi.responses import RedirectResponse

from src.utils.qr_code.qr_code_supplier_factory import QrCodeSupplierFactory

api_router = APIRouter(tags=["Test results"])


@api_router.get(
    "/qr_code/{url}",
    status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    response_class=RedirectResponse,
)
def get_qr_code(
    url: str = Path(...),
    size: int | None = Query(None, description="QR code size in pixels"),
    color: str | None = Query(None, description="QR code foreground color"),
    bg_color: str | None = Query(None, description="QR code background color"),
):
    qr_code_supplier = QrCodeSupplierFactory.create()

    query = {}
    if size:
        query['size'] = size
    if color:
        query['color'] = color
    if bg_color:
        query['bg_color'] = bg_color

    redirect_url = qr_code_supplier.generate_qr_code_link(url, **query)

    return RedirectResponse(redirect_url)
