import sqlite3


def add_nutrition_plan_to_database(student_id, nutrition_date, nutrition_plan):
    conn = sqlite3.connect('gym_helper.db')
    cursor = conn.cursor()
    table_name = f"nutrition_plans_{student_id}"
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY,
            nutrition_date DATE,
            nutrition_plan TEXT
        )
    ''')
    cursor.execute(f"SELECT * FROM {table_name} WHERE nutrition_date=?", (nutrition_date,))
    existing_nutrition = cursor.fetchone()
    if existing_nutrition:
        cursor.execute(f"UPDATE {table_name} SET nutrition_plan=? WHERE nutrition_date=?", (nutrition_plan, nutrition_date))
    else:
        cursor.execute(f"INSERT INTO {table_name} (nutrition_date, nutrition_plan) VALUES (?, ?)",
                       (nutrition_date, nutrition_plan))
    conn.commit()
    conn.close()