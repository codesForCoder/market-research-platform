from dataclasses import dataclass
from datetime import datetime

from app.models.canonical_data_model.option_contract import OptionContract


@dataclass(slots=True, frozen=True)
class OptionChainSnapshotEvent:
    underlying: str

    exchange: str

    segment: str

    expiry: datetime

    snapshot_time: datetime

    spot_price: float

    atm_strike: float | None

    total_call_oi: int

    total_put_oi: int

    total_call_volume: int

    total_put_volume: int

    contracts: list[OptionContract]
