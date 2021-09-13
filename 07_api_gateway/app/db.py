import logging
from typing import List, Dict
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from models import Currencies, Average
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from singleton import MetaSingleton
import config_loader as config_loader

logger = logging.getLogger(__name__)
config = config_loader.Config()


class DB(metaclass=MetaSingleton):
    def __init__(self):
        self.db_engine = self.__create_engine()

    def __create_engine(self) -> AsyncEngine:
        engine = create_async_engine(
            config.get(config_loader.DB_URI),
            echo=True,
        )
        return engine

    def __row_to_dict(self, row) -> Dict:
        d = {}
        for column in row.__table__.columns:
            d[column.name] = str(getattr(row, column.name))
        return d

    async def get_currencies(self, pair_name: str, limit: int) -> List[Dict]:
        async with AsyncSession(self.db_engine) as session:
            async with session.begin():
                selected_currencies_execution = await session.execute(
                    select(Currencies).filter(Currencies.pair_name == pair_name).order_by(Currencies.id.desc()).limit(
                        limit))
                selected_currencies = selected_currencies_execution.scalars().all()
                ret_data = [self.__row_to_dict(i) for i in selected_currencies]
                return ret_data

    async def get_averages(self) -> List[Dict]:
        async with AsyncSession(self.db_engine) as session:
            async with session.begin():
                selected_average_execution = await session.execute(
                    select(Average))
                selected_average = selected_average_execution.scalars().all()
                ret_data = [self.__row_to_dict(i) for i in selected_average]
                return ret_data
