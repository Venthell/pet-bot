import telebot

# Создаем объект бота с указанием токена доступа
bot = telebot.TeleBot("5463066952:AAHexYEWnfDgsALA93ym15YD2GbvZu8_Img")

# Обработчик команды start
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Я бот, который может узнать user_id пользователя в Telegram. Перешлите мне сообщение от пользователя, и я скажу вам его user_id.")

# Обработчик пересланных сообщений
@bot.message_handler(content_types=['text'])
def handle_forwarded_message(message):
    if message.forward_from is not None:
        user_id = message.forward_from.id
        bot.send_message(message.chat.id, f"User ID: {user_id}")

# Запускаем бота
bot.polling()
