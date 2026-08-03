import httpx

from app.core.config import get_settings

http_client = httpx.AsyncClient(
    timeout=get_settings().HTTP_TIMEOUT_SECONDS,
)
