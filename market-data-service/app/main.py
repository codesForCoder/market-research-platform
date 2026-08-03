from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn

from app.api.global_api_exception_handler import init_exception_handlers
from app.api.health import router as health_router
from app.api.instrument_api import router as instrument_route
from app.api.option_chain_api import router as option_chain_route
from app.core.config import get_settings
from app.core.lifecycle import startup
from app.core.lifecycle import shutdown


@asynccontextmanager
async def lifespan(app: FastAPI):

    await startup()

    yield

    await shutdown()


app = FastAPI(title="Market Data Service", version="1.0.0", lifespan=lifespan)
app.include_router(health_router)
app.include_router(instrument_route)
app.include_router(option_chain_route)
# added global exception handler
init_exception_handlers(app)

if __name__ == "__main__":
    settings = get_settings()
    uvicorn.run(
        # "app.main:app",
        app,
        host=settings.api_host,
        port=settings.api_port,
        # reload=True
    )
