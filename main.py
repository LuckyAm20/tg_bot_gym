import telebot
from dotenv import load_dotenv
import os
from gym_bot_project.databases.create_general_table import create_table
from gym_bot_project.functions import save_video, view_videos
from gym_bot_project.functions.nutrition_plan import nutrition_plan
from gym_bot_project.functions.start import start
from gym_bot_project.functions.trainer_student import handle_role_selection
from gym_bot_project.functions.view_students import view_students
from gym_bot_project.functions.training_plan import workout_plan, workout_plan_callback, custom_date_callback, handle_custom_date
from gym_bot_project.functions.add_student import add_student
from gym_bot_project.functions.gpt_request import GPTRequest
from gym_bot_project.functions.choose_trainer import choose_trainer
load_dotenv()
bot = telebot.TeleBot(os.getenv("TELEGRAM_API_TOKEN"))


@bot.message_handler(commands=['start'])
def start_main(message):
    start(message, bot)


@bot.message_handler(func=lambda message: message.text in ["Тренер", "Ученик"])
def handle_role_selection_main(message):
    handle_role_selection(message, bot)


@bot.message_handler(func=lambda message: message.text == "Выбрать тренера")
def choose_trainer_main(message):
    choose_trainer(message, bot)


@bot.message_handler(func=lambda message: message.text == "Добавить ученика")
def add_student_main(message):
    add_student(message, bot)


@bot.message_handler(func=lambda message: message.text == "Просмотреть учеников")
def view_all_students_main(message):
    view_students(message, bot)


@bot.message_handler(func=lambda message: message.text == "План тренировок")
def workout_plan_main(message):
    workout_plan(message, bot)


@bot.message_handler(func=lambda message: message.text == "План питания")
def nutrition_plan_main(message):
    nutrition_plan(message, bot)


@bot.message_handler(func=lambda message: message.text == "Запрос в GPT")
def send_gpt_request(message):
    GPTRequest(os.getenv("OPEN_API_KEY")).send_gpt_request(message, bot)


@bot.message_handler(content_types=['video'])
def save_video_main(message):
    save_video(message, bot)


@bot.message_handler(func=lambda message: message.text == "Видео тренировок")
def view_videos_main(message):
    view_videos(message, bot)


@bot.callback_query_handler(func=lambda call: call.data in ["week", "month", "year", "custom"])
def workout_plan_callback_handler(call):
    workout_plan_callback(call, bot)


@bot.callback_query_handler(func=lambda call: call.data in ["day", "back_plan_train"])
def workout_plan_callback_handler(call):
    custom_date_callback(call, bot)


@bot.message_handler(func=lambda message: message.text.startswith("День тренировки "))
def handle_custom_date_main(message):
    handle_custom_date(message, bot)


def main():
    try:
        create_table()
        bot.polling()
    except Exception:
        main()


if __name__ == '__main__':
    main()
