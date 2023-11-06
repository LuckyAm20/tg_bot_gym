import telebot
from .user_roles import add_user_role, get_user_role
from gym_bot_project.students.handle_student_actions import handle_student_actions
from gym_bot_project.trainers.handle_trainer_actions import handle_trainer_actions


def handle_role_selection(message, bot):
    user_id = message.from_user.id
    if get_user_role(user_id):
        bot.reply_to(message, "Ваша роль уже выбрана.")
    else:
        role = message.text
        username = message.from_user.username
        add_user_role(user_id, role, username)
        remove_keyboard = telebot.types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, "Вы выбрали роль " + role, reply_markup=remove_keyboard)

        if role == "Тренер":
            handle_trainer_actions(bot, user_id)
        elif role == "Ученик":
            handle_student_actions(bot, user_id)
