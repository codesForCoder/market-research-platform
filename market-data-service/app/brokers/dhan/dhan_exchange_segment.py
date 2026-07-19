from enum import IntEnum, StrEnum


class ExchangeSegment(StrEnum):
    """Exchange segment identifiers for Dhan market data.

    Each segment represents a specific market category on an exchange with a corresponding numeric value.

    Attributes:
        IDX_I: Index segment (Value: 0, Exchange: Index, Segment: Index)
        NSE_EQ: NSE Equity Cash segment (Value: 1, Exchange: NSE, Segment: Equity Cash)
        NSE_FNO: NSE Futures & Options segment (Value: 2, Exchange: NSE, Segment: Futures & Options)
        NSE_CURRENCY: NSE Currency segment (Value: 3, Exchange: NSE, Segment: Currency)
        BSE_EQ: BSE Equity Cash segment (Value: 4, Exchange: BSE, Segment: Equity Cash)
        MCX_COMM: MCX Commodity segment (Value: 5, Exchange: MCX, Segment: Commodity)
        BSE_CURRENCY: BSE Currency segment (Value: 7, Exchange: BSE, Segment: Currency)
        BSE_FNO: BSE Futures & Options segment (Value: 8, Exchange: BSE, Segment: Futures & Options)
    """

    IDX_I = "IDX_I"
    NSE_EQ = "NSE_EQ"
    NSE_FNO = "NSE_FNO"
    NSE_CURRENCY = "NSE_CURRENCY"
    BSE_EQ = "BSE_EQ"
    MCX_COMM = "MCX_COMM"
    BSE_CURRENCY = "BSE_CURRENCY"
    BSE_FNO = "BSE_FNO"