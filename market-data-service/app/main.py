from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.health import router as health_router
from app.core.lifecycle import startup
from app.core.lifecycle import shutdown


@asynccontextmanager
async def lifespan(app: FastAPI):

    await startup()

    yield

    await shutdown()


app = FastAPI(
    title="Market Data Service",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(health_router)