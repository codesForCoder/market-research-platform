import random
from collections import Counter
from typing import Iterable, List

from fastapi import APIRouter, Depends, HTTPException, status
from loguru import logger

from app.api.request_response.instrument_api_request import MarketDepthRequest, MarketFeedRequest
from app.api.request_response.instrument_api_response import (
    InstrumentElement,
    InstrumentResponseByExchangeSegment,
    InstrumentResponseById,
    MarketDepthResponse,
    MarketFeedResponse,
    SubscriptionStatus,
)
from app.bootstrap import repository_manager, subscription_manager, subscription_manager_20, subscription_manager_200
from app.market_data.subscription_manager import SubscriptionManager
from app.models.exchange import Exchange
from app.models.instrument import Instrument
from app.models.instrument_id import InstrumentId
from app.models.segment import Segment
from app.models.websocket_client_type import WebsocketClientType
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


def get_subscription_manager() -> SubscriptionManager:
    return subscription_manager


@router.post(
    "/subscribe/feed",
    summary="Subscribe to market feed",
    status_code=status.HTTP_200_OK,
    response_model=MarketFeedResponse,
)
async def subscribe_feed(
    request: MarketFeedRequest,
    repository: InstrumentRepository = Depends(get_repository),
    subs_manager: SubscriptionManager = Depends(get_subscription_manager),
) -> MarketFeedResponse:
    logger.info("Subscribing to market feed {}", request)
    instruments: list[Instrument] = [
        repository.get_by_instrument_id(
            InstrumentId(
                security_id=inst.security_id,
                segment=inst.segment,
                exchange=inst.exchange,
            )
        )
        for inst in request.instruments
    ]
    result = await subs_manager.subscribe(instruments=instruments)
    response = MarketFeedResponse(subscription_status=[item.to_status() for item in result])
    return response


@router.delete(
    "/unsubscribe/feed",
    summary="Unsubscribe from market feed",
    status_code=status.HTTP_200_OK,
    response_model=MarketFeedResponse,
)
async def unsubscribe_instruments(
    request: MarketFeedRequest,
    repository: InstrumentRepository = Depends(get_repository),
    subs_manager: SubscriptionManager = Depends(get_subscription_manager),
) -> MarketFeedResponse:
    instruments: list[Instrument] = [
        repository.get_by_instrument_id(
            InstrumentId(
                security_id=inst.security_id,
                segment=inst.segment,
                exchange=inst.exchange,
            )
        )
        for inst in request.instruments
    ]

    result = await subs_manager.unsubscribe(instruments)
    response = MarketFeedResponse(subscription_status=[item.to_status() for item in result])
    return response


@router.post(
    "/subscribe/depth",
    summary="Subscribe to market depth",
    status_code=status.HTTP_200_OK,
    response_model=MarketDepthResponse,
)
async def subscribe_feed(
    request: MarketDepthRequest,
    repository: InstrumentRepository = Depends(get_repository),
    subs_manager: SubscriptionManager = Depends(get_subscription_manager),
):
    instruments: List[Instrument] = repository.get_by_exchange_segment(
        exchange=Exchange.NSE, segment=Segment.DERIVATIVES
    )
    sample_size = min(5, len(instruments))
    random_instruments = random.sample(instruments, k=sample_size)
    await subs_manager.subscribe(instruments=random_instruments)
    return {"message": "Subscribed successfully", "subscribeInstruments": list(random_instruments)}


@router.delete(
    "/unsubscribe/depth",
    summary="Unsubscribe from market depth",
    status_code=status.HTTP_200_OK,
    response_model=MarketDepthResponse,
)
async def unsubscribe_instruments(
    request: MarketDepthRequest,
    repository: InstrumentRepository = Depends(get_repository),
    subs_manager: SubscriptionManager = Depends(get_subscription_manager),
):
    instruments: List[Instrument] = repository.get_by_exchange_segment(
        exchange=Exchange.NSE, segment=Segment.DERIVATIVES
    )
    sample_size = min(30, len(instruments))
    random_instruments = random.sample(instruments, k=sample_size)

    await subs_manager.unsubscribe(random_instruments)
    return {"message": "Unsubscribed successfully", "unsubscribeInstruments": list(random_instruments)}


@router.get("/stats", summary="Get repository stats", status_code=status.HTTP_200_OK)
def repository_stats(
    repository: InstrumentRepository = Depends(get_repository),
):

    exchange_segments_count = []
    repo_iter: Iterable[Instrument] = iter(repository)
    counts = Counter()
    for instrument in repo_iter:
        counts[(instrument.exchange, instrument.segment)] += 1

    for (exchange, segment), count in counts.items():
        exchange_segments_count.append({"exchange": exchange, "segment": segment, "count": count})

    return {
        "total_instruments": len(repository),
        "exchange_segments_count": exchange_segments_count,
    }


@router.get("/subscriptions", summary="websocket subscriptions", status_code=status.HTTP_200_OK)
async def subscriptions():
    return {
        "5_level": subscription_manager.subscription_count_per_client,
        "20_level": subscription_manager_20.subscription_count_per_client,
        "200_level": subscription_manager_200.subscription_count_per_client,
    }


@router.get("/subscriptions/{websocket_type}/{client_id}")
async def subscriptions(websocket_type: WebsocketClientType, client_id: str):
    match websocket_type:
        case WebsocketClientType.MARKET_FEED_WITH_5_DEPTH:
            data = subscription_manager.subscriptions_by_client(client_id)
        case WebsocketClientType.MARKET_DEPTH_20:
            data = subscription_manager_20.subscriptions_by_client(client_id)
        case WebsocketClientType.MARKET_DEPTH_200:
            data = subscription_manager_200.subscriptions_by_client(client_id)

    logger.info("Fetched data - {}", data)
    return data


@router.get(
    "/id", summary="get instrument details by id", status_code=status.HTTP_200_OK, response_model=InstrumentResponseById
)
def get_by_instrument_id(
    exchange: Exchange,
    segment: Segment,
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

    return InstrumentResponseById(
        instrument=InstrumentElement(
            exchange=instrument.exchange,
            segment=instrument.segment,
            security_id=instrument.security_id,
            custom_symbol_name=instrument.custom_symbol,
        )
    )


@router.get(
    "/exchange-segment",
    summary="Get instruments by exchange and segment",
    status_code=status.HTTP_200_OK,
    response_model=InstrumentResponseByExchangeSegment,
)
def get_by_exchange_segment(
    exchange: Exchange,
    segment: Segment,
    limit: int = 100,
    offset: int = 0,
    repository: InstrumentRepository = Depends(get_repository),
):

    instruments = repository.get_by_exchange_segment(exchange, segment)
    paginated_list = instruments[offset : offset + limit]
    response = InstrumentResponseByExchangeSegment(
        instruments=[
            InstrumentElement(
                exchange=data.exchange,
                segment=data.segment,
                security_id=data.security_id,
                custom_symbol_name=data.custom_symbol,
            )
            for data in paginated_list
        ],
        total_count=len(instruments),
        exchange=exchange,
        segment=segment,
        limit=limit,
        offset=offset,
    )
    return response
