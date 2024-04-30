import telebot
import psycopg2

bot = telebot.TeleBot("6990521857:AAGwG10cfmZAQ_xQ87eeyAU3HTn4dJ7f2NI")
databaseConnection = psycopg2.connect(dbname="app", user='app_user', password="jaeQuu7ziweeci5e", host="db", port="5432")
databaseConnection.close()

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
    if message.text == "Рефералочки":
        # make a request to base
        # find admin with less hit count
        # redirect to him
        pass

# Запуск бота
bot.polling()
