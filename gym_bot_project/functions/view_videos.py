from gym_bot_project.bot_data import bot
from gym_bot_project.students import get_student_id_by_username
from gym_bot_project.functions import get_user_role
from gym_bot_project.students.view_student_videos import view_student_videos_by_date


def view_videos(message):
    user_id = message.from_user.id

    if get_user_role(user_id) == "Тренер":
        bot.send_message(user_id, "Введите username ученика для просмотра его видео:")
        bot.register_next_step_handler(message, process_view_student_videos)
    elif get_user_role(user_id) == "Ученик":
        bot.send_message(user_id, "Для загрузки видео просто отправьте их в чат после")
        process_view_student_videos(message)
    else:
        bot.send_message(user_id, "Эта опция доступна только тренерам и ученикам.")


def process_view_student_videos(message):
    user_id = message.from_user.id
    student_username = message.text
    student_id = get_student_id_by_username(student_username)
    if get_user_role(user_id) == "Ученик":
        student_username = message.from_user.username
        student_id = message.from_user.id

    if student_id is not None:
        bot.send_message(user_id, "Введите дату для просмотра видео в формате ГГГГ-ММ-ДД:")
        bot.register_next_step_handler(message, view_student_videos_by_date, student_id, student_username)
    else:
        bot.send_message(user_id, f"Ученика с username {student_username} не существует.")
