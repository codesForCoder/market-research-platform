from functools import lru_cache
from pathlib import Path
import os
from loguru import logger
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ENV : str = os.getenv("APP_ENV", "local")
    model_config = SettingsConfigDict(
        env_file=[
            Path(__file__).parent.parent.parent / f".env.{ENV}",  # Checked FIRST (Overrides .env)
            Path(__file__).parent.parent.parent / ".env",  # Checked SECOND (Fallback)
        ],
        env_file_encoding="utf-8",
        extra="ignore",
    )
    logger.info("Loading settings from {}", model_config)
    #kafka
    kafka_bootstrap_servers: str
    kafka_username: str
    kafka_password: str
    kafka_ca_cert_path: str
    # Dhan
    DHAN_CLIENT_ID: str
    DHAN_ACCESS_TOKEN: str
    DHAN_FULL_MARKET_DATA_5_DEPTH_CLIENT_CAPACITY: int
    DHAN_FULL_MARKET_DATA_20_DEPTH_CLIENT_CAPACITY: int
    DHAN_FULL_MARKET_DATA_200_DEPTH_CLIENT_CAPACITY: int
    DHAN_5_DEPTH_WEBSOCKET_ALLOCATION: int
    DHAN_20_DEPTH_WEBSOCKET_ALLOCATION: int
    DHAN_200_DEPTH_WEBSOCKET_ALLOCATION: int
    DHAN_OPTION_API_POLLING_INTERVAL: int
    BASE_DIR : Path = Path(__file__).resolve().parent.parent.parent
    DHAN_INSTRUMENT_MASTER_URL: str
    HTTP_TIMEOUT_SECONDS: int
    DATA_DIRECTORY : Path = BASE_DIR / "data"
    INSTRUMENT_DIRECTORY: Path = DATA_DIRECTORY / "instruments"
    INSTRUMENT_DOWNLOAD_RETRIES: int
    INSTRUMENT_RETRY_DELAY_SECONDS: int
    INSTRUMENT_MASTER_FILE: str
    SEED_INSTRUMENT_MASTER_FILE: str
    SEED_DIRECTORY: Path = (
        BASE_DIR
        / "app"
        / "brokers"
        / "dhan"
        / "seed_master_data"
    )

    #scheduler
    INSTRUMENT_REFRESH_HOUR: int
    INSTRUMENT_REFRESH_MINUTE: int
    TIMEZONE: str


    # API
    api_host: str
    api_port: int

    # Logging
    log_level: str


@lru_cache
def get_settings() -> Settings:
    return Settings()
