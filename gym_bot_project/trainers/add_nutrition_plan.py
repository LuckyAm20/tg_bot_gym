import datetime

from gym_bot_project.bot_data import bot
from gym_bot_project.databases.add_plan_to_database import add_plan_to_database
from gym_bot_project.relations.is_valid_student_id_for_trainer import is_valid_student_id_for_trainer
from gym_bot_project.students.get_student_id import get_student_id_by_username


def add_nutrition_plan(message):
    user_id = message.from_user.id
    student_username = message.text
    student_id = get_student_id_by_username(student_username)
    if student_id is not None:
        if is_valid_student_id_for_trainer(user_id, student_id):
            bot.send_message(user_id, "Введите дату для плана питания в формате ГГГГ-ММ-ДД:")
            bot.register_next_step_handler(message, process_nutrition_date_for_plan, student_id, student_username)
        else:
            bot.send_message(user_id,
                             f"Вы не можете добавить план питания для ученика с username {student_username}.")
    else:
        bot.send_message(user_id, f"Ученика с username {student_username} не существует.")


def process_nutrition_date_for_plan(message, student_id, student_username):
    user_id = message.from_user.id
    nutrition_date = message.text
    try:
        nutrition_date = datetime.datetime.strptime(nutrition_date, '%Y-%m-%d').date()
        bot.send_message(user_id, "Введите план питания на данный день:")
        bot.register_next_step_handler(message, save_nutrition_plan, student_id, nutrition_date, student_username)
    except ValueError:
        bot.send_message(user_id, "Некорректный формат даты. Пожалуйста, введите дату в формате ГГГГ-ММ-ДД.")
        bot.register_next_step_handler(message, process_nutrition_date_for_plan, student_id, student_username)


def save_nutrition_plan(message, student_id, nutrition_date, student_username):
    user_id = message.from_user.id
    nutrition_plan = message.text
    add_plan_to_database(student_id, 'nutrition', nutrition_date, nutrition_plan)
    bot.send_message(user_id, f"План питания для ученика с username {student_username} на {nutrition_date} сохранен.")
