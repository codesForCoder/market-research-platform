from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent.parent.parent / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
    # Dhan
    dhan_client_id: str
    dhan_access_token: str
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
