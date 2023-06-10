from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from .base import BaseModel


class User(BaseModel):
    __tablename__ = 'users'

    tg_id = Column(Integer, nullable=False, unique=True)
    active_group_id = Column(Integer, ForeignKey('groups.id'))

    # relationships
    active_group = relationship('Group', backref='active_users', foreign_keys=[active_group_id])
    groups = relationship(
        'Group',
        secondary='user_group',
        back_populates='users'
    )
