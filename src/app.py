from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import src.api.health as api_health
from src import logger
from src.config.server import ServerConfig
from src.container import Container


def create_app() -> FastAPI:
    load_dotenv()

    container = Container()

    app = FastAPI(title="Template API server")
    add_cors(app=app, cfg=container.server_config())

    app.container = container  # type: ignore[attr-defined]
    app.include_router(api_health.router)

    if container.health().is_healthy():
        logger.info("is healthy!")
    else:
        logger.error("failed health check")
    return app


def add_cors(app, cfg: ServerConfig):
    logger.warning(f"CORS: {cfg.cors}")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cfg.cors.origins,
        allow_credentials=cfg.cors.allow_credentials,
        allow_methods=cfg.cors.allow_methods,
        allow_headers=cfg.cors.allow_headers,
    )
