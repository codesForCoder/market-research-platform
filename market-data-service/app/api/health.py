from datetime import datetime
from typing import Any

import psutil
from fastapi import APIRouter, HTTPException, status

# from pympler import muppy
# from pympler.summary import print_, summarize
from app.bootstrap import kafka_producer

router = APIRouter()


@router.get("/health", summary="Health Check", response_model=dict[str, str], status_code=status.HTTP_200_OK)
async def health():

    return {"status": "UP"}


@router.get("/metrics", summary="System Metrics", response_model=dict[str, Any], status_code=status.HTTP_200_OK)
async def metrics():
    process = psutil.Process()
    memory_info = process.memory_info()

    # all_objects = muppy.get_objects()
    # sum1 = summarize(all_objects)
    # print_(sum1)

    return {
        "cpu_percent": process.cpu_percent(interval=0.1),
        "memory_rss_mb": memory_info.rss / 1024 / 1024,
        "memory_percent": process.memory_percent(),
        "num_threads": process.num_threads(),
        "num_connections": len(process.net_connections()),
    }


@router.post("/kafka", summary="Test Kafka Connection", response_model=dict[str, str], status_code=status.HTTP_200_OK)
async def test_kafka():

    try:
        await kafka_producer.publish(
            topic="test-topic",
            key="test",
            value={
                "message": "Hello from Market Research Platform!",
                "timestamp": datetime.now().isoformat(),
                "status": "SUCCESS",
            },
        )

        return {"status": "Message sent successfully"}

    except Exception as ex:
        raise HTTPException(
            status_code=500,
            detail=str(ex),
        )
