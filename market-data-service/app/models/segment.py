from enum import StrEnum


class Segment(StrEnum):
    EQUITY = "E"
    DERIVATIVES = "D"
    CURRENCY = "C"
    INDEX = "I"
    COMMODITY = "M"
