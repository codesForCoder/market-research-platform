from collections import Counter, defaultdict
from itertools import chain
from typing import Any, Dict, Iterable, List

from fastapi import APIRouter, Depends, HTTPException, status
from loguru import logger

from app.api.request_response.instrument_api_request import MarketDepthRequest, MarketFeedRequest
from app.api.request_response.instrument_api_response import (
    DepthSubscriptionStatus,
    InstrumentElement,
    InstrumentResponseByExchangeSegment,
    InstrumentResponseById,
    MarketDepthResponse,
    MarketFeedResponse,
    SubscribedInstrumentsResponse,
)
from app.bootstrap import repository_manager, subscription_manager_5, subscription_manager_20, subscription_manager_200
from app.market_data.subscription_manager import SubscriptionManager
from app.models.dedicated_feed_depth import MarketDepthType
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


def get_subscription_manager_5_depth() -> SubscriptionManager:
    return subscription_manager_5


def get_subscription_manager_20_depth() -> SubscriptionManager:
    return subscription_manager_20


def get_subscription_manager_200_depth() -> SubscriptionManager:
    return subscription_manager_200


@router.post(
    "/subscribe/feed",
    summary="Subscribe to market feed",
    status_code=status.HTTP_200_OK,
    response_model=MarketFeedResponse,
)
async def subscribe_feed(
    request: MarketFeedRequest,
    repository: InstrumentRepository = Depends(get_repository),
    subs_manager: SubscriptionManager = Depends(get_subscription_manager_5_depth),
) -> MarketFeedResponse:
    logger.info("Subscribing to market feed {}", request)
    instruments: set[Instrument] = [
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
    subs_manager: SubscriptionManager = Depends(get_subscription_manager_5_depth),
) -> MarketFeedResponse:
    instruments: set[Instrument] = [
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
async def subscribe_depth(
    request: MarketDepthRequest,
    repository: InstrumentRepository = Depends(get_repository),
    subs_manager_20: SubscriptionManager = Depends(get_subscription_manager_20_depth),
    subs_manager_200: SubscriptionManager = Depends(get_subscription_manager_200_depth),
) -> MarketDepthResponse:

    instrument_depth_dict: dict[MarketDepthType, set[Instrument]] = defaultdict(set)
    for depth_input in request.instruments:
        instrument_depth_dict[depth_input.depth].add(
            repository.get_by_instrument_id(
                InstrumentId(
                    security_id=depth_input.instrument.security_id,
                    segment=depth_input.instrument.segment,
                    exchange=depth_input.instrument.exchange,
                )
            )
        )
    instruments_20_depth = instrument_depth_dict[MarketDepthType.TWENTY_LEVEL_DEPTH]
    instruments_200_depth = instrument_depth_dict[MarketDepthType.TWO_HUNDRED_LEVEL_DEPTH]
    logger.info("Subscribing to market depth with 20 depth {}", instruments_20_depth)
    logger.info("Subscribing to market depth with 200 depth {}", instruments_200_depth)

    result_20_depth = await subs_manager_20.subscribe(instruments=instruments_20_depth)
    result_200_depth = await subs_manager_200.subscribe(instruments=instruments_200_depth)

    logger.info("Subscribed to market depth with 20 depth {}", result_20_depth)
    logger.info("Subscribed to market depth with 200 depth {}", result_200_depth)

    subscription_status: list[DepthSubscriptionStatus] = []
    for result in chain(result_20_depth, result_200_depth):
        subscription_status.append(
            DepthSubscriptionStatus(
                instrument=InstrumentElement(
                    security_id=result.instrument.security_id,
                    segment=result.instrument.segment,
                    exchange=result.instrument.exchange,
                    custom_symbol_name=result.instrument.custom_symbol,
                ),
                depth=result.depth,
                is_subscribed=result.success,
                feedback=result.error,
            )
        )
    return MarketDepthResponse(subscription_status=subscription_status)


@router.delete(
    "/unsubscribe/depth",
    summary="Unsubscribe from market depth",
    status_code=status.HTTP_200_OK,
    response_model=MarketDepthResponse,
)
async def unsubscribe_depth(
    request: MarketDepthRequest,
    repository: InstrumentRepository = Depends(get_repository),
    subs_manager_20: SubscriptionManager = Depends(get_subscription_manager_20_depth),
    subs_manager_200: SubscriptionManager = Depends(get_subscription_manager_200_depth),
) -> MarketDepthResponse:

    instrument_depth_dict: dict[MarketDepthType, set[Instrument]] = defaultdict(set)
    for depth_input in request.instruments:
        instrument_depth_dict[depth_input.depth].add(
            repository.get_by_instrument_id(
                InstrumentId(
                    security_id=depth_input.instrument.security_id,
                    segment=depth_input.instrument.segment,
                    exchange=depth_input.instrument.exchange,
                )
            )
        )
    instruments_20_depth = instrument_depth_dict[MarketDepthType.TWENTY_LEVEL_DEPTH]
    instruments_200_depth = instrument_depth_dict[MarketDepthType.TWO_HUNDRED_LEVEL_DEPTH]
    logger.info("UnSubscribing to market depth with 20 depth {}", instruments_20_depth)
    logger.info("UnSubscribing to market depth with 200 depth {}", instruments_200_depth)
    result_20_depth = await subs_manager_20.unsubscribe(instruments=instruments_20_depth)
    result_200_depth = await subs_manager_200.unsubscribe(instruments=instruments_200_depth)

    logger.info("UnSubscribed to market depth with 20 depth {}", result_20_depth)
    logger.info("UnSubscribed to market depth with 200 depth {}", result_200_depth)

    subscription_status: list[DepthSubscriptionStatus] = []
    for result in chain(result_20_depth, result_200_depth):
        subscription_status.append(
            DepthSubscriptionStatus(
                instrument=InstrumentElement(
                    security_id=result.instrument.security_id,
                    segment=result.instrument.segment,
                    exchange=result.instrument.exchange,
                    custom_symbol_name=result.instrument.custom_symbol,
                ),
                depth=result.depth,
                is_subscribed=result.success,
                feedback=result.error,
            )
        )
    return MarketDepthResponse(subscription_status=subscription_status)


@router.get("/stats", summary="Get repository stats", status_code=status.HTTP_200_OK)
def repository_stats(
    repository: InstrumentRepository = Depends(get_repository),
) -> Dict[str, Any]:

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
async def subscriptions() -> Dict[str, Any]:
    return {
        "5_level": subscription_manager_5.subscription_count_per_client,
        "20_level": subscription_manager_20.subscription_count_per_client,
        "200_level": subscription_manager_200.subscription_count_per_client,
    }


@router.get(
    "/subscriptions/{websocket_type}/{client_id}",
    summary="Get Subscription details of a client",
    status_code=status.HTTP_200_OK,
    response_model=SubscribedInstrumentsResponse,
)
async def subscriptions_by_client(
    websocket_type: WebsocketClientType,
    client_id: str,
    repository: InstrumentRepository = Depends(get_repository),
) -> SubscribedInstrumentsResponse:
    instrument_ids: List[InstrumentId] = []
    match websocket_type:
        case WebsocketClientType.MARKET_FEED_WITH_5_DEPTH:
            instrument_ids = subscription_manager_5.subscriptions_by_client(client_id)
        case WebsocketClientType.MARKET_DEPTH_20:
            instrument_ids = subscription_manager_20.subscriptions_by_client(client_id)
        case WebsocketClientType.MARKET_DEPTH_200:
            instrument_ids = subscription_manager_200.subscriptions_by_client(client_id)

    instruments = [repository.get_by_instrument_id(instrument_id) for instrument_id in instrument_ids]
    response = SubscribedInstrumentsResponse(
        instruments=[
            InstrumentElement(
                segment=instrument.segment,
                exchange=instrument.exchange,
                security_id=instrument.security_id,
                custom_symbol_name=instrument.custom_symbol,
            )
            for instrument in instruments
        ],
        total_count=len(instruments),
    )
    return response


@router.get(
    "/id", summary="get instrument details by id", status_code=status.HTTP_200_OK, response_model=InstrumentResponseById
)
def get_by_instrument_id(
    exchange: Exchange,
    segment: Segment,
    security_id: int,
    repository: InstrumentRepository = Depends(get_repository),
) -> InstrumentResponseById:

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
