from gym_bot_project.bot_data import Session
from gym_bot_project.databases.tables import Relation


def is_relation_exist(student_id, trainer_id):
    session = Session()
    result = session.query(Relation).filter_by(student_id=student_id, trainer_id=trainer_id).first()
    session.close()
    return result is not None
