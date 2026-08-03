from enum import StrEnum


class InstrumentType(StrEnum):
    """Instrument type identifiers for Dhan market data.

    Each instrument type represents a specific financial instrument category available for trading.

    Attributes:
        INDEX: Index instruments
        FUTIDX: Futures of Index
        OPTIDX: Options of Index
        EQUITY: Equity instruments
        FUTSTK: Futures of Stock
        OPTSTK: Options of Stock
        FUTCOM: Futures of Commodity
        OPTFUT: Options of Commodity Futures
        FUTCUR: Futures of Currency
        OPTCUR: Options of Currency
    """

    # Cash market
    EQUITY = "EQUITY"
    INDEX = "INDEX"

    # Equity derivatives
    FUTURE_INDEX = "FUTIDX"
    FUTURE_STOCK = "FUTSTK"

    OPTION_INDEX = "OPTIDX"
    OPTION_STOCK = "OPTSTK"

    # Currency derivatives
    FUTURE_CURRENCY = "FUTCUR"
    OPTION_CURRENCY = "OPTCUR"

    # Commodity derivatives
    FUTURE_COMMODITY = "FUTCOM"

    # Options on futures (MCX)
    OPTION_FUTURE = "OPTFUT"
