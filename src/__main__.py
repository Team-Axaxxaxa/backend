from logging import getLogger
from urllib.parse import urlparse

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run

from src.handlers import list_of_routes
from src.utils.settings import Settings, get_settings

logger = getLogger(__name__)


def bind_routes(application: FastAPI, setting: Settings) -> None:
    for route in list_of_routes:
        application.include_router(route, prefix=setting.PATH_PREFIX)


def get_app() -> FastAPI:
    application = FastAPI(
        title='Test MMPI',
        docs_url='/swagger',
        openapi_url='/openapi',
        version='1.0.0',
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    settings = get_settings()
    bind_routes(application, settings)
    application.state.settings = settings
    return application


app = get_app()


if __name__ == '__main__':  # pragma: no cover
    settings_for_application = get_settings()
    run(
        'src.__main__:app',
        host=urlparse(settings_for_application.APP_HOST).netloc,
        port=settings_for_application.APP_PORT,
        reload=True,
        reload_dirs=['src', 'tests'],
        log_level='debug',
    )
