import sqlite3
import telebot

from gym_bot_project.bot_data import Session, bot
from gym_bot_project.databases.tables import Role
from gym_bot_project.students.handle_student_actions import handle_student_actions
from gym_bot_project.trainers.handle_trainer_actions import handle_trainer_actions


def start(message):
    user = message.from_user
    if user.username is None:
        bot.send_message(user.id, "Для использования бота, пожалуйста, установите username в настройках Telegram.")
        bot.send_message(user.id, "Как только вы установите username, напишите любое сообщение для продолжения.")
        bot.register_next_step_handler(message, check_username_set)
    else:
        user_id = user.id
        session = Session()
        result = session.query(Role).filter_by(user_id=user_id).first()
        session.close()

        if result:
            role = result.role
            bot.reply_to(message, f"Привет, {user.first_name}! Ваша роль уже выбрана: {role}.")
            if role == "Тренер":
                handle_trainer_actions(user_id)
            elif role == "Ученик":
                handle_student_actions(user_id)
        else:
            keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2)
            trainer_button = telebot.types.KeyboardButton(text="Тренер")
            student_button = telebot.types.KeyboardButton(text="Ученик")
            keyboard.add(trainer_button, student_button)
            bot.send_message(user_id, f"Привет, {user.first_name}! Выберите вашу роль:", reply_markup=keyboard)


def check_username_set(message):
    user = message.from_user
    if user.username is None:
        bot.send_message(user.id, "Пожалуйста, установите username в настройках Telegram.")
        bot.register_next_step_handler(message, check_username_set)
    else:
        start(message)
