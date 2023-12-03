import sqlite3


def save_video_link(user_id, video_url, upload_date):
    conn = sqlite3.connect('gym_helper.db')
    cursor = conn.cursor()

    table_name = f"videos_{user_id}"

    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY,
            video_url TEXT,
            upload_date TEXT
        )
    ''')

    cursor.execute(f"INSERT INTO {table_name} (video_url, upload_date) VALUES (?, ?)", (video_url, upload_date))
    conn.commit()
    conn.close()