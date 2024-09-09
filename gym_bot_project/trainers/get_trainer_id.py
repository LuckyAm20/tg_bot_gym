import sqlite3

from gym_bot_project.bot_data import Session
from gym_bot_project.databases.tables import Role


def get_trainer_id_by_username(username):
    session = Session()
    result = session.query(Role).filter(
        Role.username == username,
        Role.role == 'Тренер'
    ).first()
    session.close()
    return result.user_id if result else None

