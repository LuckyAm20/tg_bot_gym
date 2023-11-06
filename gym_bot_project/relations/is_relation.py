import sqlite3


def is_relation_exist(student_id, trainer_id):
    conn = sqlite3.connect('gym_helper.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM relations WHERE student_id=? AND trainer_id=?", (student_id, trainer_id))
    result = cursor.fetchone()
    conn.close()
    return result is not None
