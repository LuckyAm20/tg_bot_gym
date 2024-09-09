import sqlite3

from gym_bot_project.bot_data import Session
from gym_bot_project.databases.tables import Relation


def has_trainer(student_id):
    session = Session()
    result = session.query(Relation).filter_by(student_id=student_id).first()
    session.close()
    return result is not None
