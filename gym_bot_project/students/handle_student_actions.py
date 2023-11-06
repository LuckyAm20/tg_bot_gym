import telebot


def handle_student_actions(bot, user_id):
    student_keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2)
    student_keyboard.add("План тренировок", "Выбрать тренера", "Задать вопрос", "Отчеты")
    bot.send_message(user_id, "Вот ваши действия как ученика:", reply_markup=student_keyboard)
