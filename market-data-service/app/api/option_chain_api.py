from loguru import logger
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.api_business_exception import AppBusinessException
from app.api.request_response.option_chain_request import OptionChainRequest
from app.api.request_response.option_chain_response import OptionChainSubscriptionResponse, \
    SubscriptionInstrumentResponse, OptionChainUnSubscribeResponse
from app.bootstrap import option_chain_manager, repository_manager
from app.market_data.option_chain_manager import OptionChainManager
from app.models.instrument_id import InstrumentId
from app.repository.instrument_repository import InstrumentRepository

router = APIRouter(prefix="/option-chains", tags=["Option Chains"])


def get_option_chain_manager() -> OptionChainManager:
    return option_chain_manager


def get_repository() -> InstrumentRepository:
    if not repository_manager.is_loaded():
        raise HTTPException(
            status_code=503,
            detail="Instrument repository not loaded yet. Please wait for startup to complete.",
        )
    return repository_manager.get()


@router.post(
    "/subscribe", summary="Subscribe to option chain",
    status_code=status.HTTP_201_CREATED,
    response_model=OptionChainSubscriptionResponse,
    response_model_include={
        "status": True,
        "instrument": {"custom_symbol_name", "exchange", "segment"}
    }
)
async def subscribe(
        request: OptionChainRequest,
        manager: OptionChainManager = Depends(get_option_chain_manager),
        repository: InstrumentRepository = Depends(get_repository),
):
    instrument_id = InstrumentId(
        security_id=request.security_id,
        exchange=request.exchange,
        segment=request.segment,
    )
    instrument = repository.get_by_instrument_id(
        instrument_id=instrument_id,
    )
    if not instrument:
        raise AppBusinessException(
            error_code="OPTION_CHAIN_SUBSCRIPTION_NOT_FOUND",
            message=f"Instrument not found for instrument id: {instrument_id}",
            status_code=status.HTTP_404_NOT_FOUND
        )
    try:
        added = await manager.subscribe(instrument)

        if not added:
            raise AppBusinessException(
                error_code="OPTION_CHAIN_SUBSCRIPTION_CONFLICT",
                message="Option chain already subscribed.",
                status_code=status.HTTP_409_CONFLICT
            )

        return OptionChainSubscriptionResponse(
            instrument=SubscriptionInstrumentResponse(
                security_id=instrument.security_id,
                exchange=instrument.exchange,
                segment=instrument.segment,
                custom_symbol_name=instrument.custom_symbol,
            ),
            status="success",
        )
    except Exception as e:
        raise AppBusinessException(
            error_code="OPTION_CHAIN_SUBSCRIPTION_FAILED",
            message=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@router.delete(
    "/unsubscribe", summary="Unsubscribe from option chain",
    status_code=status.HTTP_200_OK,
    response_model=OptionChainUnSubscribeResponse,
    response_model_include={
        "status": True,
        "instrument": {"custom_symbol_name", "exchange", "segment"}
    })
async def unsubscribe(
        request: OptionChainRequest,
        manager: OptionChainManager = Depends(get_option_chain_manager),
        repository: InstrumentRepository = Depends(get_repository),
):
    instrument_id = InstrumentId(
        security_id=request.security_id,
        exchange=request.exchange,
        segment=request.segment,
    )
    instrument = repository.get_by_instrument_id(
        instrument_id=instrument_id,
    )
    if not instrument:
        raise AppBusinessException(
            error_code="OPTION_CHAIN_SUBSCRIPTION_NOT_FOUND",
            message=f"Instrument not found for instrument id: {instrument_id}",
            status_code=status.HTTP_404_NOT_FOUND
        )
    try:
        removed = await manager.unsubscribe(instrument)

        if not removed:
            raise AppBusinessException(
                error_code="OPTION_CHAIN_SUBSCRIPTION_NOT_FOUND",
                message="Option chain subscription not found.",
                status_code=status.HTTP_404_NOT_FOUND
            )

        return OptionChainUnSubscribeResponse(
            instrument=SubscriptionInstrumentResponse(
                security_id=instrument.security_id,
                exchange=instrument.exchange,
                segment=instrument.segment,
                custom_symbol_name=instrument.custom_symbol,
            ),
            status="success",
        )
    except Exception as e:
        raise AppBusinessException(
            error_code="OPTION_CHAIN_UN_SUBSCRIPTION_FAILED",
            message=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@router.get("/subscriptions", summary="Get active option subscriptions",
            response_model=List[OptionChainSubscriptionResponse],
            response_model_include={"__all__": {"instrument": {"custom_symbol_name", "exchange", "segment"}
                                                }
                                    }
            )
async def get_subscriptions(
        manager: OptionChainManager = Depends(get_option_chain_manager),
):
    subscriptions = await manager.get_subscriptions()
    logger.info("Subscriptions: {}", subscriptions)
    return [
        OptionChainSubscriptionResponse(
            instrument=SubscriptionInstrumentResponse(
                security_id=instrument.security_id,
                exchange=instrument.exchange,
                segment=instrument.segment,
                custom_symbol_name=instrument.custom_symbol,
            )
        )
        for instrument in subscriptions
    ]
