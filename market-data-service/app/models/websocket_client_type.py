from enum import StrEnum


class WebsocketClientType(StrEnum):
    MARKET_FEED_WITH_5_DEPTH = "market_feed_with_5_depth"
    MARKET_DEPTH_20 = "market_depth_20"
    MARKET_DEPTH_200 = "market_depth_200"
