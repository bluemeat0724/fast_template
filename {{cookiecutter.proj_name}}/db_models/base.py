from typing import List
from sqlalchemy.orm import declarative_base, registry, declared_attr
from sqlalchemy import UniqueConstraint, Column, Integer, String, BigInteger, Numeric, DateTime, JSON, inspect
from datetime import datetime
from sqlalchemy.dialects.mysql import insert

Base = declarative_base()


class ModelBase(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True)

    created_at = Column(DateTime, nullable=True, comment="创建时间", default=datetime.now, index=True)
    updated_at = Column(DateTime, nullable=True, comment="更新时间", default=datetime.now, onupdate=datetime.now,
                        index=True)
