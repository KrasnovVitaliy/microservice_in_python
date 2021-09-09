from fastapi import APIRouter, HTTPException
import config_loader as config_loader
import random
import metrics

config = config_loader.Config()

router = APIRouter()


@router.get("/pairs", tags=["demo"])
async def get_pairs():
    metrics.GET_PAIRS_COUNT.inc()
    return {
        "USDRUB": round(random.random() * 100, 2),
        "EURRUB": round(random.random() * 100, 2)
    }
