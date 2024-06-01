# Подключение библиотек
import telebot
import requests
import json
import sqlite3
from telebot import types 

# Подключение бота
bot = telebot.TeleBot('6622934137:AAFKQwaUYIItogSWdkxUwn6gjOp0SNaEpn4')
API = '80ed4263619171fd614122439316cf8d' #Ключ API
# Обработка функции при старте
@bot.message_handler(commands=['start'])
def start(message):
    conn = sqlite3.connect('tinkoffBot.sql')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS users (id int auto increment primary key, name varchar(20), subs BOOLEAN)')
    bot.send_message(message.chat.id, '+++')
    cur.close()
    conn.close()
    bot.send_message(message.chat.id, 'Здравствуй! Я твой ИИ помощник по бизнес вопросам в Тинькофф. Задай свой вопрос:')

# Обработка запроса пользователя
@bot.message_handler(content_types=['text'])
def get_request(message):
    keyboard = types.InlineKeyboardMarkup() 
    name = message.from_user.first_name
    subs = True

    conn = sqlite3.connect('tinkoffBot.sql')
    cur = conn.cursor() 

    cur.execute("INSERT INTO users (name, subs) VALUES ('%s', '%s')" % (message.from_user.first_name, subs))
    conn.commit()

    cur.close()
    conn.close()

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardMarkup('список пользователей', callback_data='users'))
    bot.send_message(message.chat.id, name, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    conn = sqlite3.connect('tinkoffBot.sql')
    cur = conn.cursor()

    cur.execute('SELECT * FROM users')
    users = cur.fetchall()

    info = ''
    for el in users:
        info += f'Имя: {el[1]}'
        
    cur.close()
    conn.close()

    bot.send_message(call.message.chat.id, info)



#     qestion = message.text.strip().lower()
#     res = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={qestion}&appid={API}&units=metric') #Запрос к API нейросети и получение ответа
# # Обработка запроса если он выполнен, либо произошла ошибка
#     if res.status_code == 200:
#         data = json.loads(res.text)
#         bot.reply_to(message, f'{data['main']['temp']}')
#     else:
#         bot.reply_to(message, f'Ошибка запроса: "{qestion}"')
  
bot.polling(none_stop=True)