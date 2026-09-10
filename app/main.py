import logging

from fastapi import FastAPI

from app.api.v1.health import router as health_router
from app.api.v1.incidents import router as incidents_router
from app.core.config import get_settings
from app.core.logging import setup_logging


settings = get_settings()

setup_logging()

logger = logging.getLogger(__name__)


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    debug=settings.debug,
)


app.include_router(
    health_router,
    prefix="/api/v1",
    tags=["Health"],
)

app.include_router(
    incidents_router,
    prefix="/api/v1",
    tags=["Incidents"],
)


@app.on_event("startup")
async def startup_event():
    logger.info("NEXUS API starting")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("NEXUS API shutting down")