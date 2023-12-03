import telebot
from dotenv import load_dotenv
import os
from gym_bot_project.databases.create_general_table import create_table
from gym_bot_project.functions import save_video, view_videos
from gym_bot_project.functions.nutrition_plan import nutrition_plan
from gym_bot_project.functions.start import start
from gym_bot_project.functions.trainer_student import handle_role_selection
from gym_bot_project.functions.view_students import view_students
from gym_bot_project.functions.training_plan import workout_plan
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


def main(bot):
    create_table()
    bot.polling()


if __name__ == '__main__':
    main(bot)
