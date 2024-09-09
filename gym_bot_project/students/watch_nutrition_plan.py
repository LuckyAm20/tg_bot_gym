from datetime import datetime, timedelta

from gym_bot_project.bot_data import Session, bot
from gym_bot_project.databases.tables import Plan


def watch_nutrition_plan(message):
    user_id = message.from_user.id
    user_username = message.from_user.username

    if user_id is not None:
        session = Session()
        today = datetime.now()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        nutrition_plans = session.query(Plan).filter(
            Plan.user_id == user_id,
            Plan.plan_type == 'nutrition',
            Plan.plan_date.between(start_of_week.date(), end_of_week.date())
        ).all()

        session.close()

        if nutrition_plans:
            response = f"Ваш план питания на текущую неделю с {start_of_week.date()} по {end_of_week.date()}:\n"
            for plan in nutrition_plans:
                response += f"Дата: {plan.plan_date}, План: {plan.plan}\n"
            bot.send_message(user_id, response)
        else:
            bot.send_message(user_id, "У вас пока нет плана питания на текущую неделю.")
    else:
        bot.send_message(user_id, f"Ученика с username {user_username} не существует.")
