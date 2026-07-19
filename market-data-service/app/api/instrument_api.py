from collections import Counter
import random
from typing import Iterable, List
from loguru import logger
from fastapi import APIRouter, Depends, HTTPException

from app.bootstrap import repository_manager, subscription_manager
from app.market_data.subscription_manager import SubscriptionManager
from app.models.exchange import Exchange
from app.models.instrument import Instrument
from app.models.instrument_id import InstrumentId
from app.models.segment import Segment
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
def get_subscription_manager() -> SubscriptionManager :
    return subscription_manager

@router.post("/subscribe")
async def subscribe_instruments(
        repository: InstrumentRepository = Depends(get_repository),
        subs_manager: SubscriptionManager = Depends(get_subscription_manager),
):
    instruments : List[Instrument] = repository.get_by_exchange_segment(
        exchange=Exchange.NSE,
        segment=Segment.DERIVATIVES
    )
    sample_size = min(5, len(instruments))
    random_instruments = random.sample(instruments, k=sample_size)
    least_busy_client = subs_manager.get_least_busy_client()
    await subs_manager.subscribe(
        client=least_busy_client,
        instruments=random_instruments
    )
    return {"message": "Subscribed successfully",
            "subscribeInstruments": list(random_instruments)}


@router.post("/unsubscribe")
async def unsubscribe_instruments(
        repository: InstrumentRepository = Depends(get_repository),
        subs_manager: SubscriptionManager = Depends(get_subscription_manager),
):
    instruments : List[Instrument] = repository.get_by_exchange_segment(
        exchange=Exchange.NSE,
        segment=Segment.DERIVATIVES
    )
    sample_size = min(30, len(instruments))
    random_instruments = random.sample(instruments, k=sample_size)

    await subs_manager.unsubscribe(random_instruments)
    return {"message": "Unsubscribed successfully",
            "unsubscribeInstruments": list(random_instruments)}

@router.get("/stats")
def repository_stats(
    repository: InstrumentRepository = Depends(get_repository),
):
    #This is a playground api for finding stuffs
    # This will be used for all kind of data retrival dry run
    # exchange_segments_count = []
    # repo_iter : Iterable[Instrument] = iter(repository)
    # counts = Counter()
    # for instrument in repo_iter :
    #     counts[(instrument.exchange,instrument.segment)] +=1
    #
    # for (exchange, segment), count in counts.items():
    #     exchange_segments_count.append({
    #         "exchange": exchange,
    #         "segment": segment,
    #         "count": count
    #     })

    market_feed_clients = subscription_manager.clients()
    for client in market_feed_clients:
        logger.info(f"Client: {client.unique_id}")
        client.debug()



    return {
        "total_instruments": len(repository),
         #"exchange_segments_count": exchange_segments_count,
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