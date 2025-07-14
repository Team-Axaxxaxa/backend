import abc

from urllib.parse import urlencode, urlunparse


class QrCodeSupplier(abc.ABC):
    @abc.abstractmethod
    def generate_qr_code_link(self, data: str, **kwargs) -> str:
        pass


class SimpleQrCodeSupplier(QrCodeSupplier):
    def generate_qr_code_link(
            self,
            data: str,
            color: str = '000000',
            bg_color: str = 'FFFFFF',
            size: int = 150,
            **kwargs
    ) -> str:
        query_params = {
            'data': data,
            'color': color,
            'bgcolor': bg_color,
            'size': f'{size}x{size}'
        }

        encoded_params = urlencode(query_params)
        full_url = urlunparse(('https', 'api.qrserver.com', '/v1/create-qr-code/', '', encoded_params, ''))
        return full_url
