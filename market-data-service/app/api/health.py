import psutil
from fastapi import APIRouter
from pympler import asizeof, muppy
from pympler.summary import summarize , print_

from app.bootstrap import subscription_manager

router = APIRouter()


@router.get("/health")
async def health():

    return {
        "status": "UP"
    }

@router.get("/subscriptions")
async def subscriptions():
    return subscription_manager.subscription_count_per_client

@router.get("/subscriptions/{client_id}")
async def subscriptions(client_id: str):
    return subscription_manager.subscriptions_by_client(client_id)

@router.get("/metrics")
async def metrics():
    process = psutil.Process()
    memory_info = process.memory_info()

    all_objects = muppy.get_objects()
    sum1 = summarize(all_objects)
    print_(sum1)

    return {
        "cpu_percent": process.cpu_percent(interval=0.1),
        "memory_rss_mb": memory_info.rss / 1024 / 1024,
        "memory_percent": process.memory_percent(),
        "num_threads": process.num_threads(),
        "num_connections": len(process.net_connections()),
    }