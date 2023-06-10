from sqlalchemy import Column, Integer, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship

from .base import BaseModel


class Group(BaseModel):
    __tablename__ = 'groups'

    name = Column(String(32))
    private = Column(Boolean, default=True)
    owner_id = Column(Integer, ForeignKey('users.id'))

    # relationships
    expenses = relationship('Expense', backref='group', uselist=True)
    incomes = relationship('Income', backref='group', uselist=True)
    owner = relationship(
        'User',
        backref='owner_groups',
        foreign_keys=[owner_id],
    )
    users = relationship(
        'User',
        secondary='user_group',
        back_populates='groups'
    )
