from enum import IntEnum


class ResponseCode(IntEnum):
    INDEX_PACKET = 1
    TICKER_PACKET = 2

    QUOTE_PACKET = 4
    OI_PACKET = 5
    PREVIOUS_CLOSE_PACKET = 6
    MARKET_STATUS_PACKET = 7
    FULL_PACKET = 8

    FEED_DISCONNECT = 50