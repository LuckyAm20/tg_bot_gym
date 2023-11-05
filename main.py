import telebot
import sqlite3
import datetime
import requests
deepai_api_key = '7ec4f233-4340-4975-b3c8-bcd00df7fe9d'


bot = telebot.TeleBot('6526395657:AAHJSODAFWPnJN1o6SxVt11OlQ5Jc-wec-4')


def create_table():
    conn = sqlite3.connect('gym_helper.db')
    cursor = conn.cursor()
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS roles (
            user_id INTEGER PRIMARY KEY,
            role TEXT,
            username TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS relations (
            student_id INTEGER,
            trainer_id INTEGER,
            FOREIGN KEY(student_id) REFERENCES roles(user_id),
            FOREIGN KEY(trainer_id) REFERENCES roles(user_id)
        )
    ''')
    conn.commit()
    conn.close()


def add_user_role(user_id, role, username):
    conn = sqlite3.connect('gym_helper.db')
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO roles (user_id, role, username) VALUES (?, ?, ?)", (user_id, role, username))
    conn.commit()
    conn.close()


def get_user_role(user_id):
    conn = sqlite3.connect('gym_helper.db')
    cursor = conn.cursor()
    cursor.execute("SELECT role FROM roles WHERE user_id=?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None


@bot.message_handler(commands=['start'])
def start(message):
    user = message.from_user
    if user.username is None:
        bot.send_message(user.id, "Для использования бота, пожалуйста, установите username в настройках Telegram.")
        bot.send_message(user.id, "Как только вы установите username, напишите любое сообщение для продолжения.")
        bot.register_next_step_handler(message, check_username_set)
    else:
        user_id = user.id
        conn = sqlite3.connect('gym_helper.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM roles WHERE user_id=?", (user_id,))
        result = cursor.fetchone()
        conn.close()

        if result:
            role = result[1]
            bot.reply_to(message, f"Привет, {user.first_name}! Ваша роль уже выбрана: {role}.")
            if role == "Тренер":
                handle_trainer_actions(user_id)
            elif role == "Ученик":
                handle_student_actions(user_id)
        else:
            keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2)
            trainer_button = telebot.types.KeyboardButton(text="Тренер")
            student_button = telebot.types.KeyboardButton(text="Ученик")
            keyboard.add(trainer_button, student_button)
            bot.send_message(user_id, f"Привет, {user.first_name}! Выберите вашу роль:", reply_markup=keyboard)


def check_username_set(message):
    user = message.from_user
    if user.username is None:
        bot.send_message(user.id, "Пожалуйста, установите username в настройках Telegram.")
        bot.register_next_step_handler(message, check_username_set)
    else:
        start(message)


@bot.message_handler(func=lambda message: message.text in ["Тренер", "Ученик"])
def handle_role_selection(message):
    user_id = message.from_user.id
    if get_user_role(user_id):
        bot.reply_to(message, "Ваша роль уже выбрана.")
    else:
        role = message.text
        username = message.from_user.username
        add_user_role(user_id, role, username)
        remove_keyboard = telebot.types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, "Вы выбрали роль " + role, reply_markup=remove_keyboard)

        if role == "Тренер":
            handle_trainer_actions(user_id)
        elif role == "Ученик":
            handle_student_actions(user_id)


def handle_trainer_actions(user_id):
    trainer_keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2)
    trainer_keyboard.add("Добавить упражнение", "Просмотреть учеников", "План тренировок", "Отчеты", "Добавить ученика", "Запрос в GPT")
    bot.send_message(user_id, "Вот ваши действия как тренера:", reply_markup=trainer_keyboard)


def handle_student_actions(user_id):
    student_keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2)
    student_keyboard.add("План тренировок", "Выбрать тренера", "Задать вопрос", "Отчеты")
    bot.send_message(user_id, "Вот ваши действия как ученика:", reply_markup=student_keyboard)


@bot.message_handler(func=lambda message: message.text == "Выбрать тренера")
def choose_trainer(message):
    user_id = message.from_user.id
    if get_user_role(user_id) != "Ученик":
        bot.reply_to(message, "Только ученики могут выбирать тренера.")
    elif not has_trainer(user_id):
        bot.send_message(user_id, "Введите username тренера, которого вы хотите выбрать:")
        bot.register_next_step_handler(message, process_choose_trainer)
    else:
        bot.send_message(user_id, "У вас уже есть тренер.")


def process_choose_trainer(message):
    user_id = message.from_user.id
    trainer_username = message.text
    trainer_id = get_trainer_id_by_username(trainer_username)

    if trainer_id is not None:
        if not is_relation_exist(user_id, trainer_id):
            conn = sqlite3.connect('gym_helper.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO relations (student_id, trainer_id) VALUES (?, ?)", (user_id, trainer_id))
            conn.commit()
            conn.close()
            bot.send_message(user_id, f"Тренер {trainer_username} был выбран!")
            replace_keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2)
            replace_keyboard.add("План тренировок", "Диалог с тренером", "Задать вопрос", "Отчеты")
            bot.send_message(user_id, "Теперь вы можете перейти в диалог с тренером.", reply_markup=replace_keyboard)
        else:
            bot.send_message(user_id, "Связь между вами и этим тренером уже существует.")
    else:
        bot.send_message(user_id, f"Тренера с username {trainer_username} не существует.")


def has_trainer(student_id):
    conn = sqlite3.connect('gym_helper.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM relations WHERE student_id=?", (student_id,))
    result = cursor.fetchone()
    conn.close()
    return result is not None


def is_relation_exist(student_id, trainer_id):
    conn = sqlite3.connect('gym_helper.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM relations WHERE student_id=? AND trainer_id=?", (student_id, trainer_id))
    result = cursor.fetchone()
    conn.close()
    return result is not None


def get_trainer_id_by_username(username):
    conn = sqlite3.connect('gym_helper.db')
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM roles WHERE username=? AND role='Тренер'", (username,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None


@bot.message_handler(func=lambda message: message.text == "Добавить ученика")
def add_student(message):
    user_id = message.from_user.id
    if get_user_role(user_id) != "Тренер":
        bot.reply_to(message, "Только тренеры могут добавлять учеников.")
    else:
        bot.send_message(user_id, "Введите username ученика, которого вы хотите добавить:")
        bot.register_next_step_handler(message, process_add_student)


def is_student_linked_to_another_trainer(student_id, trainer_id):
    conn = sqlite3.connect('gym_helper.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM relations WHERE student_id=? AND trainer_id!=?", (student_id, trainer_id))
    existing_relation = cursor.fetchone()
    conn.close()
    return existing_relation is not None


def process_add_student(message):
    user_id = message.from_user.id
    student_username = message.text
    student_id = get_student_id_by_username(student_username)
    if student_id is not None:
        conn = sqlite3.connect('gym_helper.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM relations WHERE student_id=? AND trainer_id=?", (student_id, user_id))
        existing_relation = cursor.fetchone()
        if existing_relation:
            bot.send_message(user_id, f"Связь между тренером и учеником уже существует.")
        elif is_student_linked_to_another_trainer(student_id, user_id):
            bot.send_message(user_id, f"У ученика с username {student_username} уже есть другой тренер.")
        else:
            cursor.execute("INSERT INTO relations (student_id, trainer_id) VALUES (?, ?)", (student_id, user_id))
            conn.commit()
            bot.send_message(user_id, f"Ученик {student_username} был добавлен.")
        conn.close()
    else:
        bot.send_message(user_id, f"Ученика с username {student_username} не существует.")


def get_student_id_by_username(username):
    conn = sqlite3.connect('gym_helper.db')
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM roles WHERE username=? AND role='Ученик'", (username,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None


@bot.message_handler(func=lambda message: message.text == "Просмотреть учеников")
def view_all_students(message):
    user_id = message.from_user.id
    if get_user_role(user_id) != "Тренер":
        bot.reply_to(message, "Только тренеры могут просматривать учеников.")
    else:
        conn = sqlite3.connect('gym_helper.db')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT user_id, username FROM relations JOIN roles ON relations.student_id = roles.user_id WHERE relations.trainer_id = ?",
            (user_id,))
        students = cursor.fetchall()
        conn.close()

        if students:
            student_names = [f"{student[1]}" for student in students]
            all_students = "\n".join(student_names)
            bot.send_message(user_id, f"Список всех учеников:\n{all_students}")
        else:
            bot.send_message(user_id, "У вас пока нет зарегистрированных учеников.")


@bot.message_handler(func=lambda message: message.text == "План тренировок")
def input_student_id_for_workout_plan(message):
    user_id = message.from_user.id
    if get_user_role(user_id) == "Тренер":
        bot.send_message(user_id, "Введите username ученика для добавления плана тренировок:")
        bot.register_next_step_handler(message, add_workout_plan)
    elif get_user_role(user_id) == "Ученик":
        watch_workout_plan(message)
    else:
        bot.send_message(user_id,
                         "Чтобы получить доступ к плану тренировок, вам необходимо иметь статус тренера или ученика.")


def watch_workout_plan(message):
    user_id = message.from_user.id
    user_username = message.from_user.username

    if message.from_user.id is not None:
        conn = sqlite3.connect('gym_helper.db')
        cursor = conn.cursor()
        table_name = f"workout_plans_{user_id}"
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
        bot.send_message(user_id, f"Ученика с username {user_username} не существует.")


def add_workout_plan(message):
    user_id = message.from_user.id
    student_username = message.text
    student_id = get_student_id_by_username(student_username)
    if student_id is not None:
        if is_valid_student_id_for_trainer(user_id, student_id):
            bot.send_message(user_id, "Введите дату тренировки в формате ГГГГ-ММ-ДД:")
            bot.register_next_step_handler(message,
                                           lambda msg: process_workout_date_for_plan(msg, student_id, student_username))
        else:
            bot.send_message(user_id,
                             f"Вы не можете добавить план тренировки для ученика с username {student_username}.")
    else:
        bot.send_message(user_id, f"Ученика с username {student_username} не существует.")


def is_valid_student_id_for_trainer(trainer_id, student_id):
    conn = sqlite3.connect('gym_helper.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM relations WHERE trainer_id=? AND student_id=?", (trainer_id, student_id))
    result = cursor.fetchone()
    conn.close()
    return result is not None


def process_workout_date_for_plan(message, student_id, student_username):
    user_id = message.from_user.id
    workout_date = message.text
    try:
        workout_date = datetime.datetime.strptime(workout_date, '%Y-%m-%d').date()
        bot.send_message(user_id, "Введите план тренировки на данный день:")
        bot.register_next_step_handler(message,
                                       lambda msg: save_workout_plan(msg, student_id, workout_date, student_username))
    except ValueError:
        bot.send_message(user_id, "Некорректный формат даты. Пожалуйста, введите дату в формате ГГГГ-ММ-ДД.")
        bot.register_next_step_handler(message,
                                       lambda msg: process_workout_date_for_plan(msg, student_id, student_username))


def save_workout_plan(message, student_id, workout_date, student_username):
    user_id = message.from_user.id
    workout_plan = message.text
    add_workout_plan_to_database(student_id, workout_date, workout_plan)
    bot.send_message(user_id, f"План тренировки для ученика с username {student_username} на {workout_date} сохранен.")


def add_workout_plan_to_database(student_id, workout_date, workout_plan):
    conn = sqlite3.connect('gym_helper.db')
    cursor = conn.cursor()
    table_name = f"workout_plans_{student_id}"
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY,
            workout_date DATE,
            workout_plan TEXT
        )
    ''')
    cursor.execute(f"SELECT * FROM {table_name} WHERE workout_date=?", (workout_date,))
    existing_workout = cursor.fetchone()
    if existing_workout:
        cursor.execute(f"UPDATE {table_name} SET workout_plan=? WHERE workout_date=?", (workout_plan, workout_date))
    else:
        cursor.execute(f"INSERT INTO {table_name} (workout_date, workout_plan) VALUES (?, ?)",
                       (workout_date, workout_plan))
    conn.commit()
    conn.close()


@bot.message_handler(func=lambda message: message.text == "Запрос в GPT")
def send_gpt_request(message):
    user_id = message.from_user.id
    if get_user_role(user_id) == "Тренер":
        bot.send_message(user_id, "Введите ваш запрос для GPT:")
        bot.register_next_step_handler(message, process_gpt_request)
    else:
        bot.send_message(user_id, "Эта опция доступна только тренерам.")


def process_gpt_request(message):
    user_id = message.from_user.id
    request = message.text

    response = requests.post(
        "https://api.deepai.org/api/text-generator",
        data={'text': request},
        headers={'api-key': deepai_api_key}
    )

    if response.status_code == 200:
        generated_text = response.json()['output']
        bot.send_message(user_id, f"Аналог упражнения, созданный deepai.org: {generated_text}")
    else:
        bot.send_message(user_id, f"Ошибка при запросе к deepai.org: {response.text}")


def main():
    create_table()
    bot.polling()


if __name__ == '__main__':
    main()
