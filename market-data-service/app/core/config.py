from functools import lru_cache
from pathlib import Path
import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ENV : str = os.getenv("APP_ENV", "local")
    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent.parent.parent / f".env.{ENV}",
        env_file_encoding="utf-8",
        extra="ignore",
    )
    # Dhan
    DHAN_CLIENT_ID: str
    DHAN_ACCESS_TOKEN: str
    DHAN_MARKET_DATA_WS_URL: str
    WS_CONNECT_TIMEOUT_SECONDS: int = 15

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
