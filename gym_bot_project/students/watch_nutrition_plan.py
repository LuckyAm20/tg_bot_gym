import datetime
import sqlite3


def watch_nutrition_plan(message, bot):
    user_id = message.from_user.id
    user_username = message.from_user.username

    if user_id is not None:
        conn = sqlite3.connect('gym_helper.db')
        cursor = conn.cursor()

        today = datetime.datetime.now()
        start_of_week = today - datetime.timedelta(days=today.weekday())
        end_of_week = start_of_week + datetime.timedelta(days=6)

        cursor.execute('''
            SELECT plan_date, plan FROM plans
            WHERE user_id = ? AND plan_type = 'nutrition' AND plan_date BETWEEN ? AND ?
        ''', (user_id, start_of_week.date(), end_of_week.date()))

        nutrition_plans = cursor.fetchall()
        conn.close()

        if nutrition_plans:
            response = f"Ваш план питания на текущую неделю с {start_of_week.date()} по {end_of_week.date()}:\n"
            for nutrition_date, nutrition_plan in nutrition_plans:
                response += f"Дата: {nutrition_date}, План: {nutrition_plan}\n"
            bot.send_message(user_id, response)
        else:
            bot.send_message(user_id, "У вас пока нет плана питания на текущую неделю.")
    else:
        bot.send_message(user_id, f"Ученика с username {user_username} не существует.")
