import sqlite3


def get_student_videos_by_date(user_id, view_date):
    conn = sqlite3.connect('gym_helper.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT video_url, upload_date FROM videos
        WHERE user_id = ? AND DATE(upload_date) = ?
    ''', (user_id, view_date))

    videos = cursor.fetchall()
    conn.close()

    return videos

