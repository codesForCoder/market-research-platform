from loguru import logger
from app.core.logging import configure_logging

async def startup():
    configure_logging()
    logger.info("Starting Market Data Service")

    #
    # Load yesterday's instrument repository
    #

    #
    # Start APScheduler
    #

    #
    # Start websocket listener
    #

    logger.info("Startup complete")


async def shutdown():

    logger.info("Stopping Market Data Service")

    #
    # Stop scheduler
    #

    #
    # Close websocket
    #

    logger.info("Shutdown complete")