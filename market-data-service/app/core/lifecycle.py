from loguru import logger

from app.bootstrap import instrument_loader, instrument_scheduler, market_feed_manager
from app.core.http_client import http_client
from app.core.logging import configure_logging


async def startup():
    configure_logging()
    logger.info("Starting Market Data Service")

    #
    # Load yesterday's instrument repository
    #
    await instrument_loader.load()
    #
    # Start APScheduler
    #
    logger.info("Starting scheduler .....")
    await instrument_scheduler.start()
    #
    # Start websocket listener
    #
    logger.info("Starting websocket manager .....")
    await market_feed_manager.start()

    logger.info("Startup complete")


async def shutdown():

    logger.info("Stopping Market Data Service")

    #
    # Stop scheduler
    #
    logger.info("stopping scheduler .....")
    await instrument_scheduler.stop()
    #
    # Close websocket and http client
    #
    logger.info("stopping websocket manager .....")
    await market_feed_manager.stop()
    logger.info("stopping http client .....")
    await http_client.aclose()

    logger.info("Shutdown complete")