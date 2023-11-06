import sqlite3


def is_valid_student_id_for_trainer(trainer_id, student_id):
    conn = sqlite3.connect('gym_helper.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM relations WHERE trainer_id=? AND student_id=?", (trainer_id, student_id))
    result = cursor.fetchone()
    conn.close()
    return result is not None
