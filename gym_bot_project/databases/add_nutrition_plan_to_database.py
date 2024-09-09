import sqlite3


def add_plan_to_database(user_id, plan_type, plan_date, plan):
    conn = sqlite3.connect('gym_helper.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO plans (user_id, plan_type, plan_date, plan)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(user_id, plan_type, plan_date) DO UPDATE SET plan=excluded.plan
    ''', (user_id, plan_type, plan_date, plan))

    conn.commit()
    conn.close()
