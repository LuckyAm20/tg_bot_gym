import sqlite3


def add_workout_plan_to_database(student_id, workout_date, workout_plan):
    conn = sqlite3.connect('gym_helper.db')
    cursor = conn.cursor()
    table_name = f"workout_plans_{student_id}"
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY,
            workout_date DATE,
            workout_plan TEXT
        )
    ''')
    cursor.execute(f"SELECT * FROM {table_name} WHERE workout_date=?", (workout_date,))
    existing_workout = cursor.fetchone()
    if existing_workout:
        cursor.execute(f"UPDATE {table_name} SET workout_plan=? WHERE workout_date=?", (workout_plan, workout_date))
    else:
        cursor.execute(f"INSERT INTO {table_name} (workout_date, workout_plan) VALUES (?, ?)",
                       (workout_date, workout_plan))
    conn.commit()
    conn.close()
