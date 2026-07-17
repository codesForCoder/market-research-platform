import psutil
from fastapi import APIRouter

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
    
    return {
        "cpu_percent": process.cpu_percent(interval=0.1),
        "memory_rss_mb": memory_info.rss / 1024 / 1024,
        "memory_percent": process.memory_percent(),
        "num_threads": process.num_threads(),
        "num_connections": len(process.connections()),
    }