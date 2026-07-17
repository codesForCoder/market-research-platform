from app.brokers.dhan.dhan_columns import DhanColumns
from app.models.instrument import Instrument
from app.utils.parsers import (
    parse_datetime,
    parse_float,
    parse_int,
    parse_option_type,
)


class DhanInstrumentMapper:

    def map(self, row: dict[str, str]) -> Instrument:

        return Instrument(

            security_id=parse_int(
                row[DhanColumns.SECURITY_ID]
            ),

            exchange=row[DhanColumns.EXCHANGE],

            segment=row[DhanColumns.SEGMENT],

            trading_symbol=row[DhanColumns.TRADING_SYMBOL],

            custom_symbol=row[DhanColumns.CUSTOM_SYMBOL],

            symbol_name=row[DhanColumns.SYMBOL_NAME],

            instrument_type=row[DhanColumns.INSTRUMENT_NAME],

            expiry_date=parse_datetime(
                row[DhanColumns.EXPIRY_DATE]
            ),

            strike_price=parse_float(
                row[DhanColumns.STRIKE_PRICE]
            ),

            option_type=parse_option_type(
                row[DhanColumns.OPTION_TYPE]
            ),

            lot_size=parse_int(
                row[DhanColumns.LOT_UNITS]
            ),

            tick_size=float(
                row[DhanColumns.TICK_SIZE]
            ),
        )