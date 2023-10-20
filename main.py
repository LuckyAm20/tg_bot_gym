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


@bot.message_handler(commands=['start'])
def start(message):
    user = message.from_user
    user_id = user.id
    create_table()
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2)
    trainer_button = telebot.types.KeyboardButton(text="Тренер")
    student_button = telebot.types.KeyboardButton(text="Ученик")
    keyboard.add(trainer_button, student_button)
    bot.send_message(user_id, f"Привет, {user.first_name}! Выберите вашу роль:", reply_markup=keyboard)


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    if message.text == "Тренер" or message.text == "Ученик":
        role = message.text
        add_user_role(user_id, role)
        bot.reply_to(message, f"Роль {role} сохранена!")
    else:
        bot.reply_to(message, "Пожалуйста, выберите роль с помощью кнопок.")


def main():
    bot.polling()


if __name__ == '__main__':
    main()






