from typing import Dict
from fastapi import APIRouter
import config_loader as config_loader
import random
import metrics

config = config_loader.Config()

router = APIRouter()


@router.get("/pairs", tags=["pairs"])
async def get_pairs() -> Dict:
    metrics.GET_PAIRS_COUNT.inc()
    return {
        "USDRUB": round(random.random() * 100, 2),
        "EURRUB": round(random.random() * 100, 2)
    }
