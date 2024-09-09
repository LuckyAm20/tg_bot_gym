from gym_bot_project.bot_data import Session, bot
from gym_bot_project.databases.tables import Relation
from gym_bot_project.students.get_student_id import get_student_id_by_username
from gym_bot_project.relations.is_student_linked_to_another_trainer import is_student_linked_to_another_trainer


def process_add_student(message):
    user_id = message.from_user.id
    student_username = message.text
    student_id = get_student_id_by_username(student_username)

    if student_id is not None:
        session = Session()
        existing_relation = session.query(Relation).filter_by(student_id=student_id, trainer_id=user_id).first()

        if existing_relation:
            bot.send_message(user_id, f"Связь между тренером и учеником уже существует.")
        elif is_student_linked_to_another_trainer(student_id, user_id):
            bot.send_message(user_id, f"У ученика с username {student_username} уже есть другой тренер.")
        else:
            new_relation = Relation(student_id=student_id, trainer_id=user_id)
            session.add(new_relation)
            session.commit()
            bot.send_message(user_id, f"Ученик {student_username} был добавлен.")

        session.close()
    else:
        bot.send_message(user_id, f"Ученика с username {student_username} не существует.")
