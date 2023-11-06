import sqlite3


def has_trainer(student_id):
    conn = sqlite3.connect('gym_helper.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM relations WHERE student_id=?", (student_id,))
    result = cursor.fetchone()
    conn.close()
    return result is not None
