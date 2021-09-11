from typing import List, Dict
from fastapi import APIRouter
import config_loader as config_loader
import metrics
from db import DB

config = config_loader.Config()

router = APIRouter()
db = DB()


@router.get("/pairs/currencies", tags=["pairs"])
async def get_currencies(pair_name: str) -> List[Dict]:
    metrics.GET_CURRENCIES_CNT.inc()
    return await db.get_currencies(pair_name)


@router.get("/pairs/average", tags=["pairs"])
async def get_average() -> List[Dict]:
    metrics.GET_AVERAGE_CNT.inc()
    return await db.get_averages()
