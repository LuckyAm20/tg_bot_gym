import telebot
import sqlite3


bot = telebot.TeleBot('6526395657:AAHJSODAFWPnJN1o6SxVt11OlQ5Jc-wec-4')


def create_table():
    conn = sqlite3.connect('gym_helper.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS roles (
            user_id INTEGER PRIMARY KEY,
            role TEXT
        )
    ''')
    conn.commit()
    conn.close()


def add_user_role(user_id, role):
    conn = sqlite3.connect('gym_helper.db')
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO roles (user_id, role) VALUES (?, ?)", (user_id, role))
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


@bot.message_handler(func=lambda message: message.text in ["Тренер", "Ученик"])
def handle_role_selection(message):
    user_id = message.from_user.id
    if get_user_role(user_id):
        bot.reply_to(message, "Ваша роль уже выбрана.")
    else:
        role = message.text
        add_user_role(user_id, role)
        remove_keyboard = telebot.types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, "Вы выбрали роль" + role, reply_markup=remove_keyboard)
        bot.reply_to(message, f"Роль {role} сохранена!")

        if role == "Тренер":
            handle_trainer_actions(user_id)
        elif role == "Ученик":
            handle_student_actions(user_id)



def handle_trainer_actions(user_id):
    trainer_keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2)
    trainer_keyboard.add("Добавить упражнение", "Просмотреть учеников", "План тренировок", "Отчеты")
    bot.send_message(user_id, "Вы выбрали роль Тренер. Вот ваши действия как тренера:", reply_markup=trainer_keyboard)

def handle_student_actions(user_id):
    student_keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2)
    student_keyboard.add("Мои тренировки", "Просмотреть тренера", "Задать вопрос", "Отчеты")
    bot.send_message(user_id, "Вы выбрали роль Ученик. Вот ваши действия как ученика:", reply_markup=student_keyboard)


def main():
    bot.polling()


if __name__ == '__main__':
    main()






