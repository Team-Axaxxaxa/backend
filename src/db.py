from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session

from src.utils.settings import get_settings


class EngineContainer:
    def __init__(self):
        settings = get_settings()
        self.engine = create_engine(
            settings.db_link,
            isolation_level='READ COMMITTED'
        )

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(EngineContainer, cls).__new__(cls)
        return cls.instance

    def get_engine(self) -> Engine:
        return self.engine

def get_session() -> Session:
    session_maker = sessionmaker(EngineContainer().engine)
    return session_maker()
