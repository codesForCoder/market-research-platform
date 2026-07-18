import psutil
from fastapi import APIRouter
from pympler import asizeof, muppy
from pympler.summary import summarize , print_

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


@router.get("/memory-detail")
async def memory_detail():
    """Detailed memory breakdown by object type"""
    from app.bootstrap import repository_manager
    
    process = psutil.Process()
    memory_info = process.memory_info()
    all_objects = muppy.get_objects()
    sum1 = summarize(all_objects)
    print_(sum1)
    # Get repository memory if loaded
    repo_memory = {}
    if repository_manager.is_loaded():
        repo = repository_manager.get()
        repo_memory = {
            "repository_total_mb": asizeof.asizeof(repo) / 1024 / 1024,
            "by_instrument_id_mb": asizeof.asizeof(repo._by_instrument_id) / 1024 / 1024,
            "by_exchange_segment_mb": asizeof.asizeof(repo._by_exchange_segment) / 1024 / 1024,
            "exchange_segments_mb": asizeof.asizeof(repo._exchange_segments) / 1024 / 1024,
            "num_instruments": len(repo),
            "num_exchange_segments": len(repo._exchange_segments),
        }
    
    return {
        "process_memory": {
            "rss_mb": memory_info.rss / 1024 / 1024,
            "vms_mb": memory_info.vms / 1024 / 1024,
            "percent": process.memory_percent(),
        },
        "repository": repo_memory,
    }