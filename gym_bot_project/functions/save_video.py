import datetime

from gym_bot_project.bot_data import bot
from gym_bot_project.databases import save_video_link
from gym_bot_project.students import save_video_file


def save_video(message):
    user_id = message.from_user.id
    file_size = message.video.file_size

    if file_size > 5 * 1024 * 1024:
        bot.send_message(user_id, "Файл слишком большой. Максимальный размер файла 5 МБ.")
        return
    video_file = bot.get_file(message.video.file_id)

    file_path = save_video_file(user_id, video_file)

    upload_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    save_video_link(user_id, file_path, upload_date)

    bot.send_message(user_id, "Ваше видео успешно сохранено.")
