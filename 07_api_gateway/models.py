import asyncio

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import func
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy.ext.indexable import index_property
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Currencies(Base):
    __tablename__ = "currencies"
    id = Column(Integer, primary_key=True)
    create_date = Column(DateTime, server_default=func.now())
    pair_name = Column(Text, index=True)
    value = Column(Float)


class Average(Base):
    __tablename__ = "average"
    id = Column(Integer, primary_key=True)
    create_date = Column(DateTime, server_default=func.now())
    pair_name = Column(Text, index=True)
    value = Column(Float)
