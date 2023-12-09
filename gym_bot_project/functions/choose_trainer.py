import telebot

from .user_roles import get_user_role
from gym_bot_project.trainers import process_choose_trainer
from gym_bot_project.relations.has_trainer import has_trainer


def choose_trainer(message, bot):
    user_id = message.from_user.id
    if get_user_role(user_id) != "Ученик":
        bot.reply_to(message, "Только ученики могут выбирать тренера.")
    elif not has_trainer(user_id):
        bot.send_message(user_id, "Введите username тренера, которого вы хотите выбрать:")
        bot.register_next_step_handler(message, process_choose_trainer, bot)
    else:
        bot.send_message(user_id, "У вас уже есть тренер.")
        replace_keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2)
        replace_keyboard.add("План тренировок", "Видео тренировок", "План питания")
        bot.send_message(user_id, "Теперь вы можете перейти в диалог с тренером.", reply_markup=replace_keyboard)
