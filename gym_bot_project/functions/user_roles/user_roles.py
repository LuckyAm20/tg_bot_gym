from gym_bot_project.bot_data import Session
from gym_bot_project.databases.tables import Role


def add_user_role(user_id, role, username):
    session = Session()
    user = session.query(Role).filter_by(user_id=user_id).first()
    if user:
        user.role = role
        user.username = username
    else:
        new_user = Role(user_id=user_id, role=role, username=username)
        session.add(new_user)
    session.commit()
    session.close()


def get_user_role(user_id):
    session = Session()
    user_role = session.query(Role.role).filter_by(user_id=user_id).first()
    session.close()
    return user_role[0] if user_role else None
