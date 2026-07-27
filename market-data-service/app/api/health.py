import psutil
from fastapi import APIRouter
from pympler import muppy
from pympler.summary import summarize, print_

router = APIRouter()


@router.get("/health")
async def health():

    return {
        "status": "UP"
    }
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