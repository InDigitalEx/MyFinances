from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .base import BaseModel


class Income(BaseModel):
    __tablename__ = 'incomes'

    amount = Column(Integer, nullable=False)
    text = Column(String(32))
    group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    # relationships
    user = relationship('User')
