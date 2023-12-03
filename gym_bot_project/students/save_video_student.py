import datetime
import os


def save_video_file(bot, user_id, video_file):
    folder_path = create_student_video_folder(user_id)
    file_path = os.path.join(folder_path, f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.mp4")

    video_file_path = bot.download_file(video_file.file_path)
    with open(file_path, 'wb') as video:
        video.write(video_file_path)

    return file_path


def create_student_video_folder(user_id):
    folder_path = f'video/{user_id}'
    os.makedirs(folder_path, exist_ok=True)
    return folder_path
