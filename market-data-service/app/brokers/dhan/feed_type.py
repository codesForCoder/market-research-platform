from enum import Enum

from app.brokers.dhan.request_code import RequestCode


class FeedType(Enum):
    TICKER = RequestCode.SUBSCRIBE_TICKER
    QUOTE = RequestCode.SUBSCRIBE_QUOTE
    FULL = RequestCode.SUBSCRIBE_FULL
    FULL_MARKET_DEPTH = RequestCode.SUBSCRIBE_FULL_MARKET_DEPTH