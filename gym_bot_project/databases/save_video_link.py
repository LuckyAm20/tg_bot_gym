import sqlite3


def save_video_link(user_id, video_url, upload_date):
    conn = sqlite3.connect('gym_helper.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO videos (user_id, video_url, upload_date)
        VALUES (?, ?, ?)
    ''', (user_id, video_url, upload_date))

    conn.commit()
    conn.close()