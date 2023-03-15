import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Room(SqlAlchemyBase):
    __tablename__ = 'rooms'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String,
                             nullable=False, unique=True)
    started_at = sqlalchemy.Column(sqlalchemy.DateTime,
                                   nullable=True)
    time = sqlalchemy.Column(sqlalchemy.Time, nullable=False)
    max_users = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
