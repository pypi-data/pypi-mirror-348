from fastapi import FastAPI
from importlib.metadata import version as pkg_version, PackageNotFoundError

from .api import api_router
from .core.database import init_db
from .core.logger import setup_logging

try:
    __version__ = pkg_version("{{ cookiecutter.project_slug }}")
except PackageNotFoundError:
    __version__ = "0.1.0"


def create_app() -> FastAPI:
    app = FastAPI(title="{{ cookiecutter.project_slug }}", version=__version__, openapi_url="/openapi.json", docs_url="/docs")

    setup_logging()

    # 掛載聚合路由
    app.include_router(api_router)

    @app.on_event("startup")
    def _startup():
        init_db()

    return app


app = create_app() 