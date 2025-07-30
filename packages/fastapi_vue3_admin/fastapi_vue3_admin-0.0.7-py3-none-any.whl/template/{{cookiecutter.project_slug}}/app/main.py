from fastapi import FastAPI

from .api import api_router
from .core.database import init_db
from .core.logger import setup_logging


def create_app() -> FastAPI:
    app = FastAPI(title="fastapi_vue3_admin", openapi_url="/openapi.json", docs_url="/docs")

    setup_logging()

    # 掛載聚合路由
    app.include_router(api_router)

    @app.on_event("startup")
    def _startup():
        init_db()

    return app


app = create_app() 