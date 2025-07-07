from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker

from src.utils.settings import get_settings


class EngineContainer:
    def __init__(self):
        settings = get_settings().db_settings
        user = settings['user']
        password = settings['password']
        port = str(settings['port'])
        db = settings['db']
        self.engine = create_engine(
            f'postgresql+psycopg2://{user}:{password}@postgres:{port}/{db}',
            isolation_level='READ COMMITTED'
        )

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(EngineContainer, cls).__new__(cls)
        return cls.instance

    def get_engine(self) -> Engine:
        return self.engine

Session = sessionmaker(EngineContainer().engine)
