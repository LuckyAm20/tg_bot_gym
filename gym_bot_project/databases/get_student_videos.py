import sqlite3


def get_student_videos_by_date(student_id, view_date):
    conn = sqlite3.connect('gym_helper.db')
    cursor = conn.cursor()
    table_name = f"videos_{student_id}"

    cursor.execute(f"SELECT video_url, upload_date FROM {table_name} WHERE DATE(upload_date) = ?", (view_date,))
    videos = cursor.fetchall()
    conn.close()

    return videos
