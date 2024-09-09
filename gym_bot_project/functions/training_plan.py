import calendar
import datetime

from telebot import types

from gym_bot_project.bot_data import bot
from gym_bot_project.functions.user_roles import get_user_role
from gym_bot_project.students import watch_workout_plan
from gym_bot_project.students.watch_plan import view_workout_plans
from gym_bot_project.trainers import add_workout_plan


def workout_plan(message):
    user_id = message.from_user.id
    if get_user_role(user_id) == "Тренер":
        bot.send_message(user_id, "Введите username ученика для добавления плана тренировок:")
        bot.register_next_step_handler(message, add_workout_plan)
    elif get_user_role(user_id) == "Ученик":
        workout_plan_menu(user_id)
    else:
        bot.send_message(user_id,
                         "Чтобы получить доступ к плану тренировок, вам необходимо иметь статус тренера или ученика.")


def workout_plan_menu(user_id):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    week_button = types.InlineKeyboardButton(text="На следующую неделю", callback_data="week")
    month_button = types.InlineKeyboardButton(text="За предыдущий месяц", callback_data="month")
    year_button = types.InlineKeyboardButton(text="За предыдущий год", callback_data="year")
    custom_button = types.InlineKeyboardButton(text="Выбранный день", callback_data="custom")
    keyboard.add(week_button, month_button, year_button, custom_button)
    bot.send_message(user_id, "Выберите период для просмотра планов тренировок:", reply_markup=keyboard)


def workout_plan_callback(call):
    user_id = call.from_user.id

    if call.data == "week":
        watch_workout_plan(call)
    elif call.data == "month":
        view_workout_plans_for_month(user_id)
    elif call.data == "year":
        view_workout_plans_for_year(user_id)
    elif call.data == "custom":
        choose_custom_date(user_id)


def choose_custom_date(user_id):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    back_button = types.InlineKeyboardButton(text="Назад", callback_data="back_plan_train")
    day_button = types.InlineKeyboardButton(text="Выбери день", callback_data="day")
    keyboard.add(day_button, back_button)
    bot.send_message(user_id, "Выберите день для просмотра планов тренировок:", reply_markup=keyboard)


def custom_date_callback(call):
    user_id = call.from_user.id

    if call.data == "back_plan_train":
        workout_plan_menu(user_id)
    elif call.data == "day":
        bot.send_message(user_id, "Введите день для просмотра планов тренировок, формат ввода: 'День тренировки YYYY-MM-DD.'")


def handle_custom_date(message):
    user_id = message.from_user.id
    selected_date = message.text.lstrip("День тренировки ")
    try:
        parsed_date = datetime.datetime.strptime(selected_date, "%Y-%m-%d").date()

        view_workout_plans(user_id, parsed_date, parsed_date)
    except ValueError:
        bot.send_message(user_id, "Некорректный формат даты. Пожалуйста, введите дату в формате 'День тренировки YYYY-MM-DD'.")


def view_workout_plans_for_month(user_id):
    today = datetime.datetime.now().date()
    start_of_month = today.replace(day=1)
    prev_month = start_of_month - datetime.timedelta(days=1)

    if prev_month.month == 1:
        prev_month = prev_month.replace(year=prev_month.year - 1, month=12)
    else:
        prev_month = prev_month.replace(month=prev_month.month)

    prev_month_days = calendar.monthrange(prev_month.year, prev_month.month)[1]
    start_of_prev_month = prev_month.replace(day=1)
    end_of_prev_month = prev_month.replace(day=prev_month_days)
    view_workout_plans(user_id, start_of_prev_month, end_of_prev_month)


def view_workout_plans_for_year(user_id):
    today = datetime.datetime.now().date()
    current_year = today.year
    start_of_prev_year = datetime.date(current_year - 1, 1, 1)
    end_of_prev_year = datetime.date(current_year - 1, 12, 31)
    view_workout_plans(user_id, start_of_prev_year, end_of_prev_year)
