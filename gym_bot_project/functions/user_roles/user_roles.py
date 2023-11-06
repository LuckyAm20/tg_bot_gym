import sqlite3


def add_user_role(user_id, role, username):
    conn = sqlite3.connect('gym_helper.db')
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO roles (user_id, role, username) VALUES (?, ?, ?)", (user_id, role, username))
    conn.commit()
    conn.close()


def get_user_role(user_id):
    conn = sqlite3.connect('gym_helper.db')
    cursor = conn.cursor()
    cursor.execute("SELECT role FROM roles WHERE user_id=?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None
