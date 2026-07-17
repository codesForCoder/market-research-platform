from typing import Iterable
from loguru import logger
from fastapi import APIRouter, Depends, HTTPException

from app.bootstrap import repository_manager
from app.models.instrument import Instrument
from app.models.instrument_id import InstrumentId
from app.repository.instrument_repository import InstrumentRepository

router = APIRouter(
    prefix="/api/instruments",
    tags=["Instrument Repository"],
)


#
# Dependency
#
def get_repository() -> InstrumentRepository:
    if not repository_manager.is_loaded():
        raise HTTPException(
            status_code=503,
            detail="Instrument repository not loaded yet. Please wait for startup to complete.",
        )
    return repository_manager.get()


@router.get("/stats")
def repository_stats(
    repository: InstrumentRepository = Depends(get_repository),
):
    exchange_segments_count = []
    exchange_segments = repository.get_exchange_segments()
    for exchange, segment in exchange_segments:
       items = repository.get_by_exchange_segment(exchange , segment)
       exchange_segments_count.append({
           "exchange": exchange,
           "segment": segment,
           "count": len(items)
       })

    return {
        "total_instruments": len(repository),
         "exchange_segments_count": exchange_segments_count,
    }


@router.get("")
def get_by_instrument_id(
    exchange: str,
    segment: str,
    security_id: int,
    repository: InstrumentRepository = Depends(get_repository),
):

    instrument = repository.get_by_instrument_id(
        InstrumentId(
            exchange=exchange,
            segment=segment,
            security_id=security_id,
        )
    )

    if instrument is None:
        raise HTTPException(
            status_code=404,
            detail="Instrument not found",
        )

    return instrument


@router.get("/exchange-segment")
def get_by_exchange_segment(
    exchange: str,
    segment: str,
    repository: InstrumentRepository = Depends(get_repository),
):

    return repository.get_by_exchange_segment(
        exchange=exchange,
        segment=segment,
    )