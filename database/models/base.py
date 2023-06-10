from sqlalchemy import Column, Integer, DateTime, func

from database import Database


class BaseModel(Database().BASE):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime(), default=func.now())
    updated_at = Column(DateTime(), default=func.now(), onupdate=func.now())
