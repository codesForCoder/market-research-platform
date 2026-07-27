from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4
from loguru import logger
import httpx
from dhanhq import DhanContext, dhanhq

from app.brokers.dhan.expiry_dates_response_dto import DateResponseSchema
from app.brokers.dhan.exchange_segment_mapper import ExchangeSegmentMapper
from app.market_data.option_chain_client import OptionChainClient
from app.models.instrument import Instrument
from app.models.option_chain_snapshot import OptionChainSnapshot


class DhanOptionChainClient(OptionChainClient):

    def __init__(
        self,
        client_id: str,
        access_token: str,
    ) -> None:
        self._client_id = client_id
        self._access_token = access_token
        self._dhan_context: DhanContext = DhanContext(
            client_id=client_id,
            access_token=access_token,
        )
        self._dhan_client : dhanhq = dhanhq(self._dhan_context)

    async def fetch(
        self,
        instrument: Instrument,
    ) -> OptionChainSnapshot:
        exchange_segment = ExchangeSegmentMapper.to_exchange_segment(
            exchange=instrument.instrument_id.exchange,
            segment=instrument.instrument_id.segment,
        )
        #First getting the latest expiry date
        raw_response :dict[str ,Any] = self._dhan_client.expiry_list(
            under_security_id=instrument.security_id,
            under_exchange_segment=exchange_segment.value
        )
        logger.info("Expiry date response: FOR Instrument {} --> {}",instrument.custom_symbol, raw_response['data'])
        expiry_dates = DateResponseSchema.model_validate(raw_response['data']).data
        # --- FIND THE NEAREST PRESENT/FUTURE DATE ---

        # 1. Grab today's current date object
        today = datetime.today().date()
        nearest_date = None
        # 2. Filter for dates >= today, and pick the minimum (closest) value
        try:
            nearest_date = min(d for d in expiry_dates if d >= today)
            logger.info("Nearest present/future date: {}", nearest_date)
            # Based on your data list, this will accurately output: 2026-07-28
        except ValueError:
            logger.warning("There are no present or future dates available in the list.")

        response = self._dhan_client.option_chain(
            under_security_id=instrument.security_id,
            under_exchange_segment=exchange_segment.value,
            expiry=nearest_date.isoformat()
        )
        logger.info("Option chain response with status : {}", response.get('status',"Unknown"))

        return None