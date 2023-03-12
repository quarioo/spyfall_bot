import sqlalchemy
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    telegram_id = sqlalchemy.Column(sqlalchemy.Integer,
                                    nullable=False)
    room_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey('rooms.id'), nullable=True)
    is_creator = sqlalchemy.Column(sqlalchemy.Boolean,
                                   nullable=False)
