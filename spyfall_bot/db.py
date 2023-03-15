from data import db_session
from data.rooms import Room

db_session.global_init("db/games.db")


async def create_room_in_db(name, time, max_users):
    room = Room()
    room.name = name
    room.time = time
    room.max_users = max_users
    db_sess = db_session.create_session()
    db_sess.add(room)
    db_sess.commit()


async def is_room_in_db(name):
    if name != 'a':
        return True
    else:
        return False
