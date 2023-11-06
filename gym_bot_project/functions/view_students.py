import sqlite3
from gym_bot_project.functions.user_roles import get_user_role


def view_students(message, bot):
    user_id = message.from_user.id
    if get_user_role(user_id) != "Тренер":
        bot.reply_to(message, "Только тренеры могут просматривать учеников.")
    else:
        conn = sqlite3.connect('gym_helper.db')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT user_id, username FROM relations JOIN roles ON relations.student_id = roles.user_id WHERE relations.trainer_id = ?",
            (user_id,))
        students = cursor.fetchall()
        conn.close()

        if students:
            student_names = [f"{student[1]}" for student in students]
            all_students = "\n".join(student_names)
            bot.send_message(user_id, f"Список всех учеников:\n{all_students}")
        else:
            bot.send_message(user_id, "У вас пока нет зарегистрированных учеников.")
