import logging
import aiohttp
import metrics

from typing import List, Dict

logger = logging.getLogger(__name__)


class DataProvider:
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def __send_request(self, path: str, params: Dict) -> Dict:
        logger.debug("Send HTTP request")
        logger.debug(f"Full path: {path} params: {params}")
        async with aiohttp.ClientSession() as session:
            async with session.get(path, params=params) as rsp:
                if rsp.status == 200:
                    metrics.SUCCESS_RESPONSE_CNT.inc()
                    return await rsp.json()
                else:
                    metrics.ERROR_RESPONSE_CNT.inc()
                    logger.error(rsp.status)
                    logger.error(await rsp.text())
                    return {}

    async def get_pairs(self) -> Dict:
        logger.debug("Get pairs")
        rsp = await self.__send_request(path=self.base_url, params={})
        return rsp
