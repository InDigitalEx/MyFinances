from sqlalchemy import Column, ForeignKey, Table

from database import Database


user_group = Table(
    'user_group',
    Database().BASE.metadata,
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    Column('group_id', ForeignKey('groups.id'), primary_key=True)
)
