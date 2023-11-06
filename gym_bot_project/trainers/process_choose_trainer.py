import sqlite3
import telebot
from gym_bot_project.relations.is_relation import is_relation_exist
from gym_bot_project.trainers.get_trainer_id import get_trainer_id_by_username


def process_choose_trainer(message, bot):
    user_id = message.from_user.id
    trainer_username = message.text
    trainer_id = get_trainer_id_by_username(trainer_username)

    if trainer_id is not None:
        if not is_relation_exist(user_id, trainer_id):
            conn = sqlite3.connect('gym_helper.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO relations (student_id, trainer_id) VALUES (?, ?)", (user_id, trainer_id))
            conn.commit()
            conn.close()
            bot.send_message(user_id, f"Тренер {trainer_username} был выбран!")
            replace_keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2)
            replace_keyboard.add("План тренировок", "Диалог с тренером", "Задать вопрос", "Отчеты")
            bot.send_message(user_id, "Теперь вы можете перейти в диалог с тренером.", reply_markup=replace_keyboard)
        else:
            bot.send_message(user_id, "Связь между вами и этим тренером уже существует.")
    else:
        bot.send_message(user_id, f"Тренера с username {trainer_username} не существует.")
