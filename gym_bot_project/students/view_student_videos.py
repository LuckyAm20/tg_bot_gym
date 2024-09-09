import datetime
import os

from gym_bot_project.bot_data import bot
from gym_bot_project.databases import get_student_videos_by_date


def view_student_videos_by_date(message, student_id, student_username):
    user_id = message.from_user.id
    view_date = message.text

    try:
        view_date = datetime.datetime.strptime(view_date, '%Y-%m-%d').date()

        videos = get_student_videos_by_date(student_id, view_date)

        if videos:
            for video_url, upload_date in videos:
                current_directory = os.getcwd()
                video_path = os.path.join(current_directory, video_url)
                video_file = open(video_path, 'rb')
                bot.send_video(user_id, video_file, caption=f"Видео ученика {student_username} загружено {upload_date}")
                video_file.close()
        else:
            bot.send_message(user_id, f"У ученика {student_username} нет видео за {view_date}.")
    except ValueError:
        bot.send_message(user_id, "Некорректный формат даты. Пожалуйста, введите дату в формате ГГГГ-ММ-ДД.")
        bot.register_next_step_handler(message, view_student_videos_by_date, student_id, student_username)
