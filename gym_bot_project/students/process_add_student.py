import sqlite3
from gym_bot_project.students.get_student_id import get_student_id_by_username
from gym_bot_project.relations.is_student_linked_to_another_trainer import is_student_linked_to_another_trainer


def process_add_student(message, bot):
    user_id = message.from_user.id
    student_username = message.text
    student_id = get_student_id_by_username(student_username)
    if student_id is not None:
        conn = sqlite3.connect('gym_helper.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM relations WHERE student_id=? AND trainer_id=?", (student_id, user_id))
        existing_relation = cursor.fetchone()
        if existing_relation:
            bot.send_message(user_id, f"Связь между тренером и учеником уже существует.")
        elif is_student_linked_to_another_trainer(student_id, user_id):
            bot.send_message(user_id, f"У ученика с username {student_username} уже есть другой тренер.")
        else:
            cursor.execute("INSERT INTO relations (student_id, trainer_id) VALUES (?, ?)", (student_id, user_id))
            conn.commit()
            bot.send_message(user_id, f"Ученик {student_username} был добавлен.")
        conn.close()
    else:
        bot.send_message(user_id, f"Ученика с username {student_username} не существует.")
