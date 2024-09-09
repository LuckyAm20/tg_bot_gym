from datetime import datetime

from gym_bot_project.bot_data import Session
from gym_bot_project.databases.tables import Video


def save_video_link(user_id, video_url, upload_date):
    session = Session()
    upload_date = datetime.strptime(upload_date, '%Y-%m-%d').date()
    new_video = Video(user_id=user_id, video_url=video_url, upload_date=upload_date)
    session.add(new_video)
    session.commit()
    session.close()
