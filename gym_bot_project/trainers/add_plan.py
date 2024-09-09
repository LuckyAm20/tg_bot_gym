import datetime
from gym_bot_project.relations import is_valid_student_id_for_trainer
from gym_bot_project.students.get_student_id import get_student_id_by_username
from gym_bot_project.databases import add_plan_to_database


def add_workout_plan(message, bot):
    user_id = message.from_user.id
    student_username = message.text
    student_id = get_student_id_by_username(student_username)
    if student_id is not None:
        if is_valid_student_id_for_trainer(user_id, student_id):
            bot.send_message(user_id, "Введите дату тренировки в формате ГГГГ-ММ-ДД:")
            bot.register_next_step_handler(message,
                                           lambda msg: process_workout_date_for_plan(msg, bot, student_id, student_username))
        else:
            bot.send_message(user_id,
                             f"Вы не можете добавить план тренировки для ученика с username {student_username}.")
    else:
        bot.send_message(user_id, f"Ученика с username {student_username} не существует.")


def process_workout_date_for_plan(message, bot, student_id, student_username):
    user_id = message.from_user.id
    workout_date = message.text
    try:
        workout_date = datetime.datetime.strptime(workout_date, '%Y-%m-%d').date()
        bot.send_message(user_id, "Введите план тренировки на данный день:")
        bot.register_next_step_handler(message,
                                       lambda msg: save_workout_plan(msg, bot, student_id, workout_date, student_username))
    except ValueError:
        bot.send_message(user_id, "Некорректный формат даты. Пожалуйста, введите дату в формате ГГГГ-ММ-ДД.")
        bot.register_next_step_handler(message,
                                       lambda msg: process_workout_date_for_plan(msg, bot, student_id, student_username))


def save_workout_plan(message, bot, student_id, workout_date, student_username):
    user_id = message.from_user.id
    workout_plan = message.text
    add_plan_to_database(student_id, 'workout', workout_date, workout_plan)
    bot.send_message(user_id, f"План тренировки для ученика с username {student_username} на {workout_date} сохранен.")
