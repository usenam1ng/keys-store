import telebot

# Создание экземпляра бота с токеном
bot = telebot.TeleBot("6990521857:AAGwG10cfmZAQ_xQ87eeyAU3HTn4dJ7f2NI")

# Обработчик сообщений
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    # Создание текстового сообщения для ответа
    text = message.text

    # Создание клавиатуры с кнопками
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2)
    btn1 = telebot.types.KeyboardButton("Отзывы")
    btn2 = telebot.types.KeyboardButton("Тех-поддержка")
    btn3 = telebot.types.KeyboardButton("Рефералочки")
    keyboard.add(btn1, btn2, btn3)

    # Отправка сообщения с клавиатурой
    bot.send_message(message.chat.id, text, reply_markup=keyboard)

# Запуск бота
bot.polling()
