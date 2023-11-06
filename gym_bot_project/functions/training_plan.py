from gym_bot_project.functions.user_roles import get_user_role
from gym_bot_project.students import watch_workout_plan
from gym_bot_project.trainers import add_workout_plan


def input_student_id_for_workout_plan(message, bot):
    user_id = message.from_user.id
    if get_user_role(user_id) == "Тренер":
        bot.send_message(user_id, "Введите username ученика для добавления плана тренировок:")
        bot.register_next_step_handler(message, add_workout_plan, bot)
    elif get_user_role(user_id) == "Ученик":
        watch_workout_plan(message, bot)
    else:
        bot.send_message(user_id,
                         "Чтобы получить доступ к плану тренировок, вам необходимо иметь статус тренера или ученика.")
