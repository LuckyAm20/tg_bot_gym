import telebot


def handle_trainer_actions(bot, user_id):
    trainer_keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2)
    trainer_keyboard.add("Добавить упражнение", "Просмотреть учеников", "План тренировок", "Отчеты", "Добавить ученика", "Запрос в GPT")
    bot.send_message(user_id, "Вот ваши действия как тренера:", reply_markup=trainer_keyboard)
