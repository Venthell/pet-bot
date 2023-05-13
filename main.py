import telebot
import json
import base64

# создаем объект бота и указываем токен, который получили от BotFather (УКАЗАТЬ ТОКЕН БОТА ПРИ СЛУЧАЕ!)
bot = telebot.TeleBot('6256427432:AAGufNdCfIsV48oOpqnVuI42HHm2WZHHjv8')

# открываем файл с базой данных пользователей (УКАЗАТЬ ПУТЬ К БАЗЕ ДАННЫХ!)
with open('C:\\Users\\Venthell\\Desktop\\Joy Pet Bot\\data.json', 'r') as f:
    data = json.load(f)

# команда start для проверки пользователя по user_id в базе данных
@bot.message_handler(commands=['start'])
def start_handler(message):
    user_id = str(message.from_user.id)
    if user_id not in data:
        bot.reply_to(message, 'Извините, но вы не являетесь сотрудником.')
    else:
        bot.reply_to(message, 'Привет! Чтобы зарегистрировать питомца, отправьте мне его фотографию в формате изображения.')

# обработчик фотографии питомца
@bot.message_handler(content_types=['photo'])
def photo_handler(message):
    user_id = str(message.from_user.id)
    # получаем id фотографии и ее бинарные данные
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    file_data = bot.download_file(file_info.file_path)
    # кодируем бинарные данные фотографии в строку base64
    file_base64 = base64.b64encode(file_data).decode('utf-8')
    # сохраняем фотографию питомца в базу данных (УКАЗАТЬ ПУТЬ К БАЗЕ ДАННЫХ!)
    data[user_id] = {'photo': file_base64}
    with open('C:\\Users\\Venthell\\Desktop\\Joy Pet Bot\\data.json', 'w') as f:
        json.dump(data, f, indent=4)
    bot.reply_to(message, 'Фото загружено. Теперь отправьте мне описание питомца.')

# обработчик описания питомца
@bot.message_handler(func=lambda message: True)
def description_handler(message):
    user_id = str(message.from_user.id)
    description = message.text
    # сохраняем описание питомца в базу данных (УКАЗАТЬ ПУТЬ К БАЗЕ ДАННЫХ!)
    data[user_id]['description'] = description
    with open('C:\\Users\\Venthell\\Desktop\\Joy Pet Bot\\data.json', 'w') as f:
        json.dump(data, f, indent=4)
    bot.reply_to(message, 'Описание загружено. Спасибо за регистрацию!')

# функция для отправки фотографии и описания питомца в канал
def send_pet_to_channel(channel_id: -1001878261637):
    for user_id in data:
        photo_base64 = data[user_id]['photo']
        # декодируем строку base64 в бинарные данные фотографии
        photo_data = base64.b64decode(photo_base64)
        # загружаем фотографию на сервер телеграм и получаем ее id
        photo_info = bot.upload_photo(photo_data)
        photo_id = photo_info.photo[-1].file_id
        description = data[user_id]['description']
        # создаем сообщение с фотографией, описанием и кнопкой для лайков
        message = f'{description}\n\nЛайки: 0'
        markup = telebot.types.InlineKeyboardMarkup()
        like_button = telebot.types.InlineKeyboardButton('Лайк!', callback_data=f'like_{photo_id}')
        markup.add(like_button)
        # отправляем сообщение в канал
        bot.send_photo(channel_id, photo_id, caption=message, reply_markup=markup)

# запускаем бота
bot.polling()