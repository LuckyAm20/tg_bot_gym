from gym_bot_project.bot_data import Session
from gym_bot_project.databases.tables import Relation


def is_valid_student_id_for_trainer(trainer_id, student_id):
    session = Session()
    result = session.query(Relation).filter_by(trainer_id=trainer_id, student_id=student_id).first()
    session.close()
    return result is not None
