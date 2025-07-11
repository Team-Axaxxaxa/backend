from src.utils.qr_code.qr_code_supplier import SimpleQrCodeSupplier, QrCodeSupplier
from src.utils.settings import get_settings


class QrCodeSupplierFactory:
    @staticmethod
    def create() -> QrCodeSupplier:
        supplier_type = get_settings().QR_CODE_SUPPLIER

        if supplier_type == 'simple':
            return SimpleQrCodeSupplier()
        else:
            return SimpleQrCodeSupplier()
