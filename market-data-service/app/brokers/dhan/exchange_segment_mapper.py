from app.models.exchange import Exchange
from app.models.segment import Segment
from app.brokers.dhan.dhan_exchange_segment import ExchangeSegment

class ExchangeSegmentMapper:

    _mapping = {

        (
            Exchange.NSE,
            Segment.EQUITY,
        ): ExchangeSegment.NSE_EQ,

        (
            Exchange.NSE,
            Segment.DERIVATIVES,
        ): ExchangeSegment.NSE_FNO,

        (
            Exchange.NSE,
            Segment.CURRENCY,
        ): ExchangeSegment.NSE_CURRENCY,

        (
            Exchange.NSE,
            Segment.INDEX,
        ): ExchangeSegment.IDX_I,

        (
            Exchange.BSE,
            Segment.EQUITY,
        ): ExchangeSegment.BSE_EQ,

        (
            Exchange.BSE,
            Segment.DERIVATIVES,
        ): ExchangeSegment.BSE_FNO,

        (
            Exchange.BSE,
            Segment.CURRENCY,
        ): ExchangeSegment.BSE_CURRENCY,

        (
            Exchange.BSE,
            Segment.INDEX,
        ): ExchangeSegment.IDX_I,

        (
            Exchange.MCX,
            Segment.COMMODITY,
        ): ExchangeSegment.MCX_COMM,
    }

    @classmethod
    def to_exchange_segment(
        cls,
        exchange: Exchange,
        segment: Segment,
    ) -> ExchangeSegment:

        try:
            return cls._mapping[(exchange, segment)]  # type: ignore[index]
        except KeyError:
            raise ValueError(
                f"No Dhan ExchangeSegment mapping for "
                f"{exchange}/{segment}"
            )