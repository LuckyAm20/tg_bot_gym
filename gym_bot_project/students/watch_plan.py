import datetime
import sqlite3


def watch_workout_plan(message, bot):
    user_id = message.from_user.id
    user_username = message.from_user.username

    if message.from_user.id is not None:
        conn = sqlite3.connect('gym_helper.db')
        cursor = conn.cursor()
        table_name = f"workout_plans_{user_id}"

        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        existing_table = cursor.fetchone()

        if existing_table:
            today = datetime.datetime.now()
            start_of_week = today - datetime.timedelta(days=today.weekday())
            end_of_week = start_of_week + datetime.timedelta(days=6)
            cursor.execute(f"SELECT workout_date, workout_plan FROM {table_name} WHERE workout_date BETWEEN ? AND ?", (start_of_week.date(), end_of_week.date()))
            workout_plans = cursor.fetchall()
            conn.close()

            if workout_plans:
                response = f"Ваш план тренировок на текущую неделю с {start_of_week.date()} по {end_of_week.date()}:\n"
                for workout_date, workout_plan in workout_plans:
                    response += f"Дата: {workout_date}, План: {workout_plan}\n"
                bot.send_message(user_id, response)
            else:
                bot.send_message(user_id, "У вас пока нет плана тренировок на текущую неделю.")
        else:
            bot.send_message(user_id, "У вас пока нет созданных планов тренировок.")
    else:
        bot.send_message(user_id, f"Ученика с username {user_username} не существует.")


def view_workout_plans(bot, user_id, start_date, end_date):
    conn = sqlite3.connect('gym_helper.db')
    cursor = conn.cursor()
    table_name = f"workout_plans_{user_id}"

    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
    existing_table = cursor.fetchone()

    if existing_table:
        cursor.execute(f"SELECT workout_date, workout_plan FROM {table_name} WHERE workout_date BETWEEN ? AND ?", (start_date, end_date))
        workout_plans = cursor.fetchall()
        conn.close()

        if workout_plans:
            response = f"Ваш план тренировок за период с {start_date} по {end_date}:\n"
            for workout_date, workout_plan in workout_plans:
                response += f"Дата: {workout_date}, План: {workout_plan}\n"
            bot.send_message(user_id, response)
        else:
            bot.send_message(user_id, f"У вас пока нет плана тренировок за период с {start_date} по {end_date}.")
    else:
        bot.send_message(user_id, "У вас пока нет созданных планов тренировок.")
