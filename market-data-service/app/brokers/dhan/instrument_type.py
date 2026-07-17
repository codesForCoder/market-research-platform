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

    INDEX = "INDEX"

    EQUITY = "EQUITY"

    FUTIDX = "FUTIDX"
    OPTIDX = "OPTIDX"

    FUTSTK = "FUTSTK"
    OPTSTK = "OPTSTK"

    FUTCOM = "FUTCOM"
    OPTFUT = "OPTFUT"

    FUTCUR = "FUTCUR"
    OPTCUR = "OPTCUR"