from gym_bot_project.bot_data import Session
from gym_bot_project.databases.tables import Role


def get_student_id_by_username(username):
    session = Session()
    result = session.query(Role).filter_by(username=username, role='Ученик').first()
    session.close()
    return result.user_id if result else None
