import sqlite3


def get_student_id_by_username(username):
    conn = sqlite3.connect('gym_helper.db')
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM roles WHERE username=? AND role='Ученик'", (username,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None
