from loguru import logger

from app.bootstrap import (
    instrument_loader,
    instrument_scheduler,
    market_feed_manager,
    market_feed_manager_20,
    market_feed_manager_200,
    option_chain_scheduler,
    kafka_producer,
    # market_feed_manager_20,
    # market_feed_manager_200
)
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
    # Start Kafka producer
    #
    logger.info("Starting kafka producer .....")
    await kafka_producer.start()
    #
    # Start websocket listener
    #
    logger.info("Starting websocket manager .....")
    await market_feed_manager.start()
    await market_feed_manager_20.start()
    await market_feed_manager_200.start()
    logger.info("Starting option chain http client .....")
    await option_chain_scheduler.start()
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
    await market_feed_manager_20.stop()
    await market_feed_manager_200.stop()
    logger.info("stopping option chain http client .....")
    await option_chain_scheduler.stop()
    logger.info("stopping http client .....")
    await http_client.aclose()
    #
    # Stop Kafka producer
    #
    logger.info("stopping kafka producer .....")
    await kafka_producer.stop()

    logger.info("Shutdown complete")
