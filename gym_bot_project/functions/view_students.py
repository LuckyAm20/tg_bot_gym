from gym_bot_project.bot_data import Session
from gym_bot_project.databases.tables import Role, Relation


def view_students(message, bot):
    user_id = message.from_user.id
    session = Session()
    role = session.query(Role).filter_by(user_id=user_id).first()

    if role is None or role.role != "Тренер":
        bot.reply_to(message, "Только тренеры могут просматривать учеников.")
    else:
        students = session.query(Relation, Role).join(Role, Relation.student_id == Role.user_id).filter(Relation.trainer_id == user_id).all()
        session.close()

        if students:
            student_names = [f"{student[1].username}" for student in students]
            all_students = "\n".join(student_names)
            bot.send_message(user_id, f"Список всех учеников:\n{all_students}")
        else:
            bot.send_message(user_id, "У вас пока нет зарегистрированных учеников.")
