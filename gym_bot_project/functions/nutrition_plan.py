from gym_bot_project.bot_data import bot
from gym_bot_project.students import watch_nutrition_plan
from gym_bot_project.trainers import add_nutrition_plan
from gym_bot_project.functions.user_roles import get_user_role


def nutrition_plan(message):
    user_id = message.from_user.id
    if get_user_role(user_id) == "Тренер":
        bot.send_message(user_id, "Введите username ученика для добавления плана тренировок:")
        bot.register_next_step_handler(message, add_nutrition_plan)
    elif get_user_role(user_id) == "Ученик":
        watch_nutrition_plan(message)
    else:
        bot.send_message(user_id,
                         "Чтобы получить доступ к плану питания, вам необходимо иметь статус тренера или ученика.")
