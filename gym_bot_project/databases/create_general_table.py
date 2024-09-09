from gym_bot_project.bot_data import engine, Base


def create_table():
    Base.metadata.create_all(engine)
