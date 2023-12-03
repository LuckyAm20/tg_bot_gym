import datetime
import sqlite3


def watch_nutrition_plan(message, bot):
    user_id = message.from_user.id
    user_username = message.from_user.username

    if message.from_user.id is not None:
        conn = sqlite3.connect('gym_helper.db')
        cursor = conn.cursor()
        table_name = f"nutrition_plans_{user_id}"

        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        existing_table = cursor.fetchone()

        if existing_table:
            today = datetime.datetime.now()
            start_of_week = today - datetime.timedelta(days=today.weekday())
            end_of_week = start_of_week + datetime.timedelta(days=6)
            cursor.execute(f"SELECT nutrition_date, nutrition_plan FROM {table_name} WHERE nutrition_date BETWEEN ? AND ?", (start_of_week.date(), end_of_week.date()))
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
            bot.send_message(user_id, "У вас пока нет созданных планов питания.")
    else:
        bot.send_message(user_id, f"Ученика с username {user_username} не существует.")
