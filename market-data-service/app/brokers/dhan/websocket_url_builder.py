from urllib.parse import urlencode

from app.core.config import get_settings


class DhanWebSocketUrlBuilder:

    VERSION = 2
    AUTH_TYPE = 2

    @classmethod
    def build(cls) -> str:

        settings = get_settings()

        query = urlencode(
            {
                "version": cls.VERSION,
                "token": settings.DHAN_ACCESS_TOKEN,
                "clientId": settings.DHAN_CLIENT_ID,
                "authType": cls.AUTH_TYPE,
            }
        )

        return f"{settings.DHAN_MARKET_DATA_WS_URL}?{query}"