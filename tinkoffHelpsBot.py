# Подключение библиотек
import telebot
import requests
import json

# Подключение бота
bot = telebot.TeleBot('6622934137:AAFKQwaUYIItogSWdkxUwn6gjOp0SNaEpn4')
API = '80ed4263619171fd614122439316cf8d' #Ключ API

# Обработка функции при старте
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Здравсвуй! Я твой ИИ помощник по бизнес вопросам в Тинькофф. Задай свой вопрос')

# Обработка запроса пользователя
@bot.message_handler(content_types=['text'])
def get_weather(message):
    qestion = message.text.strip().lower()
    res = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={qestion}&appid={API}&units=metric') #Запрос к API нейросети и получение ответа
# Обработка запроса если он выполнен, либо произошла ошибка
    if res.status_code == 200:
        data = json.loads(res.text)
        bot.reply_to(message, f'{data['main']['temp']}')
    else:
        bot.reply_to(message, f'Ошибка запроса: "{city}"')
  
bot.polling(none_stop=True)