from gym_bot_project.bot_data import Session
from gym_bot_project.databases.tables import Relation


def is_student_linked_to_another_trainer(student_id, trainer_id):
    session = Session()
    existing_relation = session.query(Relation).filter(Relation.student_id == student_id, Relation.trainer_id != trainer_id).first()
    session.close()
    return existing_relation is not None
