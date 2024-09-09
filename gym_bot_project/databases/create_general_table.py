import sqlite3


def create_table():
    conn = sqlite3.connect('gym_helper.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS roles (
            user_id INTEGER PRIMARY KEY,
            role TEXT,
            username TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS relations (
            student_id INTEGER,
            trainer_id INTEGER,
            FOREIGN KEY(student_id) REFERENCES roles(user_id),
            FOREIGN KEY(trainer_id) REFERENCES roles(user_id)
        )
    ''')

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS plans (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                plan_type TEXT,
                plan_date DATE,
                plan TEXT,
                UNIQUE(user_id, plan_type, plan_date),
                FOREIGN KEY(user_id) REFERENCES roles(user_id)
            )
        ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS videos (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            video_url TEXT,
            upload_date TEXT,
            FOREIGN KEY(user_id) REFERENCES roles(user_id)
        )
    ''')

    conn.commit()
    conn.close()
