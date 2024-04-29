import telebot

# Создание экземпляра бота с токеном
bot = telebot.TeleBot("6990521857:AAGwG10cfmZAQ_xQ87eeyAU3HTn4dJ7f2NI")

# Обработчик сообщений
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

@bot.message_handler(commands=["_get_chat_id"])
def get_chat_id(message):
    bot.send_message(message.chat.id, str(message.chat.id))

# Запуск бота
bot.polling()
