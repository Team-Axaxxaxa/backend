from os import environ

class Settings:
    POSTGRES_DB: str = environ.get('POSTGRES_DB', 'db')
    POSTGRES_USER: str = environ.get('POSTGRES_USER', 'user')
    POSTGRES_PASSWORD: str = environ.get('POSTGRES_PASSWORD', 'password')
    POSTGRES_HOST: str = environ.get('POSTGRES_HOST', 'localhost')
    POSTGRES_PORT: int = int(environ.get('POSTGRES_PORT', 5432))

    @property
    def db_settings(self) -> dict:
        return {
            'database': self.POSTGRES_DB,
            'user': self.POSTGRES_USER,
            'password': self.POSTGRES_PASSWORD,
            'host': self.POSTGRES_HOST,
            'port': self.POSTGRES_PORT,
        }

def get_settings() -> Settings:
    return Settings()
