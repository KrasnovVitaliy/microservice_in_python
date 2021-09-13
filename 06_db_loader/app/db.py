import logging
import asyncio
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

    async def save_currency(self, pair_name: str, value: float) -> None:
        async with AsyncSession(self.db_engine) as session:
            async with session.begin():
                logger.info(f"Save currency {pair_name}: {value}")
                currency = Currencies(pair_name=pair_name, value=value)
                session.add(currency)

    async def save_average(self, pair_name: str, value: float) -> None:
        async with AsyncSession(self.db_engine) as session:
            async with session.begin():
                selected_average_execution = await session.execute(
                    select(Average).filter(Average.pair_name == pair_name))
                selected_average = selected_average_execution.scalars().first()
                if selected_average:
                    logger.info(f"Update existing average {pair_name}: {value}")
                    selected_average.value = value
                else:
                    logger.info(f"Save average {pair_name}: {value}")
                    currency = Average(pair_name=pair_name, value=value)
                    session.add(currency)


async def async_main():
    config = config_loader.Config()
    engine = create_async_engine(
        config.get(config_loader.DB_URI),
        echo=True,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Currencies.metadata.drop_all)
        await conn.run_sync(Average.metadata.drop_all)

        await conn.run_sync(Currencies.metadata.create_all)
        await conn.run_sync(Average.metadata.create_all)


if __name__ == '__main__':
    asyncio.run(async_main())
