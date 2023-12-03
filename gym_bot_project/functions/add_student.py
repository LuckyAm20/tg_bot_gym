from .user_roles import get_user_role
from gym_bot_project.students.process_add_student import process_add_student


def add_student(message, bot):
    user_id = message.from_user.id
    if get_user_role(user_id) != "Тренер":
        bot.reply_to(message, "Только тренеры могут добавлять учеников.")
    else:
        bot.send_message(user_id, "Введите username ученика, которого вы хотите добавить:")
        bot.register_next_step_handler(message, process_add_student, bot)
