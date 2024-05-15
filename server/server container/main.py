import telebot
import psycopg2
import threading
from time import sleep
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

bot = telebot.TeleBot("5000224649:AAGmCkeaxsD7ZCzPnYavep7rsOY-V9BoSsc/test")
databaseConnection = psycopg2.connect(dbname="app", user='app_user', password="jaeQuu7ziweeci5e", host="db", port="6666")
databaseCursor = databaseConnection.cursor()

def register_user(message, referral_id=None):
    cursor = databaseConnection.cursor()
    select_statement = """
        SELECT * FROM users
        WHERE chat_id = %s AND user_id = %s"""

    cursor.execute(select_statement, (message.chat.id, message.from_user.id))
    result = cursor.fetchall()

    if len(result) == 0:
        try:
            if referral_id:
                # Обрабатываем реферальный случай
                databaseCursor.execute("UPDATE users SET discount = 10 WHERE user_id = %s", (referral_id,))

                discount = 5
                insert_statement = """
                    INSERT INTO users (chat_id, user_id, bought_id, referrer_id, discount)
                    VALUES (%s, %s, %s, %s, %s)"""
                databaseCursor.execute(insert_statement, (message.chat.id, message.from_user.id, 0, referral_id, discount))

                # Добавление в таблицу referrals
                databaseCursor.execute("INSERT INTO referrals (user_id, referred_user_id) VALUES (%s, %s)", (referral_id, message.from_user.id))
            else:
                insert_statement = """
                INSERT INTO users (chat_id, user_id, bought_id)
                VALUES (%s, %s, %s)"""
                databaseCursor.execute(insert_statement, (message.chat.id, message.from_user.id, 0))

            databaseConnection.commit()
            print("registered user")
        except (Exception, psycopg2.DatabaseError) as e:
            bot.send_message(message.chat.id, str(e))
    else:
        bot.send_message(message.chat.id, "Добро пожаловать, снова.")

@bot.message_handler(commands=['iamadminnow_SUPERSECRETPASSWORD'])
def add_admin(message):
    cursor = databaseConnection.cursor()
    select_statement = """
        SELECT * FROM tech_support
        WHERE admin_chat_id = %s"""

    cursor.execute(select_statement, (message.chat.id,))
    result = cursor.fetchall()

    if len(result) == 0:
        try:
            insert_statement = """
            INSERT INTO tech_support (admin_username, admin_chat_id, hit_count)
            VALUES (%s, %s, %s)"""

            databaseCursor.execute(insert_statement, (message.from_user.username, message.chat.id, 0))
            databaseConnection.commit()

            print("added admin ", (message.from_user.username, message.chat.id, 0))
            bot.send_message(message.chat.id, "Вы теперь администратор.")
        except (Exception, psycopg2.DatabaseError) as e:
            bot.send_message(message.chat.id, str(e))
    else:
        bot.send_message(message.chat.id, "Вы уже администратор.")

# Обработчик /start с поддержкой реферальных ссылок
@bot.message_handler(commands=["start"])
def handle_start(message):
    referral_id = None
    if len(message.text.split()) > 1:
        referral_id = message.text.split()[1]

    if referral_id:
        register_user(message, referral_id=referral_id)
    else:
        register_user(message)

    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn1 = telebot.types.KeyboardButton("Отзывы")
    btn2 = telebot.types.KeyboardButton("Тех-поддержка")
    btn3 = telebot.types.KeyboardButton("Рефералочки")
    keyboard.add(btn1).row(btn2, btn3)

    bot.send_message(message.chat.id, "Привет! Добро пожаловать в наш маленький уютный магазинчик.", reply_markup=keyboard)

@bot.message_handler(commands=["getchatid"])
def get_chat_id(message):
    bot.send_message(message.chat.id, str(message.chat.id))

@bot.message_handler(content_types=['text'])
def text_message_handlers(message):
    bot.delete_message(message.chat.id, message.id)

    if message.text == "Тех-поддержка":
        try:
            databaseCursor.execute("SELECT admin_username FROM tech_support ORDER BY hit_count ASC LIMIT 1;")
            username = databaseCursor.fetchone()
            databaseCursor.execute("""UPDATE tech_support
                                        SET hit_count = hit_count + 1
                                        WHERE admin_username IN (
                                          SELECT admin_username
                                          FROM tech_support
                                          ORDER BY hit_count ASC
                                          LIMIT 1
                                        );
                                        """)
            bot.send_message(message.chat.id, f"Обратитесть к администратору: @{username[0]}")
        except (Exception, psycopg2.DatabaseError) as e:
            bot.send_message(message.chat.id, str(e))
    elif message.text == "Отзывы":
        bot.send_message(message.chat.id, "Отзывы в канале: t.me/ggstore_community/2")
    elif message.text == "Рефералочки":
        referral_link = f"https://t.me/your_bot_username?start={message.from_user.id}"
        bot.send_message(message.chat.id, f"Ваша реферальная ссылка: {referral_link}")

@bot.message_handler(content_types="web_app_data") 
def web_app_handler(message):
    print(message) 
    print(message.web_app_data.data) 
    bot.send_message("5000971271", str(message.web_app_data.data))

@app.route('/request', methods=['POST'])
def request_handler():
    data = request.get_json()
    buyType = data.get('type')
    user_id = data.get('user_id')

    if buyType not in ['rent', 'buy']:
        return jsonify({'error': 'Invalid type'}), 400

    bot.send_message("5000971271", str(data))
    try:
        select_statement = """
            SELECT chat_id
            FROM users
            WHERE user_id = %s
        """
        databaseCursor.execute(select_statement, (user_id,))
        result = databaseCursor.fetchone()

        chat_id = result[0]

        bot.send_message(chat_id, "BUTTON PUSH!!!!!:")
        bot.send_message(chat_id, str(data))

        return jsonify({'success': 'Request processed'}), 200

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error getting user's chat_id: ", error)
        return None

def start_bot():
    bot.polling()

def flask_api_server():
    app.run(host='0.0.0.0', port=9999)

if __name__ == "__main__":
    t1 = threading.Thread(target=start_bot)
    t2 = threading.Thread(target=flask_api_server)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print("All threads exited. Terminating...")