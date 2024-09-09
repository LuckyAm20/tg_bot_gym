from datetime import datetime

from gym_bot_project.bot_data import Session
from gym_bot_project.databases.tables import Video


def get_student_videos_by_date(user_id, view_date):
    session = Session()

    view_date = datetime.strptime(view_date, '%Y-%m-%d').date()

    videos = session.query(Video.video_url, Video.upload_date).filter(
        Video.user_id == user_id,
        Video.upload_date == view_date
    ).all()

    session.close()

    return videos

