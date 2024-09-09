from sqlalchemy.exc import IntegrityError

from gym_bot_project.bot_data import Session
from gym_bot_project.databases.tables import Plan


def add_plan_to_database(user_id, plan_type, plan_date, plan):
    session = Session()

    existing_plan = session.query(Plan).filter_by(user_id=user_id, plan_type=plan_type, plan_date=plan_date).first()

    if existing_plan:
        existing_plan.plan = plan
    else:
        new_plan = Plan(user_id=user_id, plan_type=plan_type, plan_date=plan_date, plan=plan)
        session.add(new_plan)

    try:
        session.commit()
    except IntegrityError:
        session.rollback()
    finally:
        session.close()

