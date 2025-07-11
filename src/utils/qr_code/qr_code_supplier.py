import abc


class QrCodeSupplier(abc.ABC):
    @abc.abstractmethod
    def generate_qr_code_link(self, data: str) -> str:
        pass


class SimpleQrCodeSupplier(QrCodeSupplier):
    def generate_qr_code_link(self, data: str) -> str:
        return f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={data}"
