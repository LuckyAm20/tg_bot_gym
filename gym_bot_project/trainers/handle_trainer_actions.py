import telebot

from gym_bot_project.bot_data import bot


def handle_trainer_actions(user_id):
    trainer_keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2)
    trainer_keyboard.add("Просмотреть учеников", "План тренировок", "План питания",
                         "Видео тренировок", "Добавить ученика", "Запрос в GPT")
    bot.send_message(user_id, "Вот ваши действия как тренера:", reply_markup=trainer_keyboard)
