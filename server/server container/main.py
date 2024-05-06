import telebot
import psycopg2
import threading
from time import sleep
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

bot = telebot.TeleBot("5000035098:AAFzHkyiU8Fso5QUlSbcWfGMJyAh2QB3ZnY/test")
databaseConnection = psycopg2.connect(dbname="app", user='app_user', password="jaeQuu7ziweeci5e", host="db", port="6666")
databaseCursor = databaseConnection.cursor()

# Обработчик /start
@bot.message_handler(commands=["start"])
def echo_all(message):
    # Создание текстового сообщения для ответа
    text = message.text

    # Создание клавиатуры с кнопками
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn1 = telebot.types.KeyboardButton("Отзывы")
    btn2 = telebot.types.KeyboardButton("Тех-поддержка")
    btn3 = telebot.types.KeyboardButton("Рефералочки")
    keyboard.add(btn1).row(btn2, btn3)

    # Отправка сообщения с клавиатурой
    bot.send_message(message.chat.id, text, reply_markup=keyboard)


# Обработчик /_get_chat_id
@bot.message_handler(commands=["getchatid"])
def get_chat_id(message):
    bot.send_message(message.chat.id, str(message.chat.id))


# Обработчик текстовых сообщений
@bot.message_handler(content_types=['text'])
def textMessageHandlers(message):
    # remove users message (thats pretty)
    bot.delete_message(message.chat.id, message.id)

    if message.text == "Тех-поддержка":
        # make a request to base
        # find admin with less hit count
        # redirect to him
        
        try:
            # Get admin with less hit_count
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
            bot.send_message(message.chat.id, f"Обратитесть к администратору: {username[0]}")
        except (Exception, psycopg2.DatabaseError) as e:
            bot.send_message(message.chat.id, str(e))
    elif message.text == "Отзывы":
        bot.send_message(message.chat.id, "Отзывы в канале: t.me/ggstore_community/2")


# Обработчик сообщений из webApp
@bot.message_handler(content_types="web_app_data") 
def webAppHandler(message):
   print(message) 
   print(message.web_app_data.data) 
   bot.send_message("5000971271", str(message.web_app_data.data))

@app.route('/request', methods=['POST'])
def request_handler():
    print("RUNNING")
    
    data = request.get_json()
    buyType = data.get('type')
    user_id = data.get('user_id')

    if buyType not in ['rent', 'buy']:
        return jsonify({'error': 'Invalid type'}), 400

    bot.send_message("5000971271", f"type={buyType};from={user_id}")
    print("sent message")
    return jsonify({'success': 'Request processed'}), 200

# Запуск бота
def startBot():
    bot.polling()

def flaskApiServer():
    print("RUNNING")
    app.run(host='0.0.0.0', port=9999)

if __name__ == "__main__":
    
    t1 = threading.Thread(target=startBot)
    t2 = threading.Thread(target=flaskApiServer)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print("All threads exited. Terminating...")