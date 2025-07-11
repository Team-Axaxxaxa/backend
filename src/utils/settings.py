from os import environ

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    POSTGRES_DB: str = environ.get('POSTGRES_DB', 'db')
    POSTGRES_USER: str = environ.get('POSTGRES_USER', 'user')
    POSTGRES_PASSWORD: str = environ.get('POSTGRES_PASSWORD', 'password')
    POSTGRES_HOST: str = environ.get('POSTGRES_HOST', 'localhost')
    POSTGRES_PORT: int = int(environ.get('POSTGRES_PORT', 5432))

    PATH_PREFIX: str = environ.get('PATH_PREFIX', '/api/v1')
    APP_HOST: str = environ.get('APP_HOST', 'http://0.0.0.0')
    APP_PORT: int = int(environ.get('APP_PORT', 8080))

    SECRET_KEY: str = environ.get('SECRET_KEY', 'secret')

    QR_CODE_SUPPLIER: str = environ.get('QR_CODE_SUPPLIER', 'simple')

    AI_MODEL: str = environ.get('AI_MODEL', 'mock')
    OPEN_ROUTER_API_KEY: str = environ.get('OPEN_ROUTER_API_KEY', 'open_api_key')

    @property
    def db_settings(self) -> dict:
        return {
            'database': self.POSTGRES_DB,
            'user': self.POSTGRES_USER,
            'password': self.POSTGRES_PASSWORD,
            'host': self.POSTGRES_HOST,
            'port': self.POSTGRES_PORT,
        }

    @property
    def db_link(self) -> str:
        user = self.POSTGRES_USER
        password = self.POSTGRES_PASSWORD
        host = self.POSTGRES_HOST
        port = str(self.POSTGRES_PORT)
        db = self.POSTGRES_DB
        return f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}'

def get_settings() -> Settings:
    return Settings()
