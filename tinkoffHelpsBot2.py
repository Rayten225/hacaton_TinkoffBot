# Подключение библиотек
import telebot
import requests
import json
import sqlite3
from telebot import types 
import os

# Подключение бота
bot = telebot.TeleBot('6622934137:AAFKQwaUYIItogSWdkxUwn6gjOp0SNaEpn4')
API = '80ed4263619171fd614122439316cf8d' #Ключ API
# Обработка функции при старте
@bot.message_handler(commands=['start'])
def start(message):
    name = message.from_user.id
    subs = 1
    conn = sqlite3.connect('tinkoffBot.sql')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS users (id int auto increment primary key, name varchar(20), subs BOOLEAN)')
    checkID = cur.execute('SELECT COUNT(*) FROM users WHERE  name =  %s'  %  name)
    results = checkID.fetchone()
    bot.send_message(message.chat.id, 'Здравствуй! Я твой ИИ помощник по бизнес вопросам в Тинькофф. Задай свой вопрос:')
    conn.commit()
    print(results)
    if results == (0,):
        cur.execute("INSERT INTO users (name, subs) VALUES ('%s', '%s')" % (message.chat.id, subs))
        conn.commit()
        print(results)
    
    cur.close()
    conn.close()
    

# Обработка запроса пользователя
@bot.message_handler(commands=['users'])
def get_request(message):
    keyboard = types.InlineKeyboardMarkup() 


    conn = sqlite3.connect('tinkoffBot.sql')
    cur = conn.cursor() 

    # checkID = cur.execute('SELECT COUNT(*) FROM users WHERE  name =  %s'  %  name)
    # results = checkID.fetchone()

    # conn.commit()
    # print(results)
    # if results == (0,):
    #     cur.execute("INSERT INTO users (name, subs) VALUES ('%s', '%s')" % (message.chat.id, subs))
    #     conn.commit()
    #     print(results)


    cur.close()
    conn.close()

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('список пользователей', callback_data='users'))
    bot.send_message(message.chat.id, name, reply_markup=markup)


@bot.message_handler(commands=['notificationsadmin1123'])
def ask_for_photo(message):
    msg = bot.send_message(message.chat.id, 'Отправьте фото:')
    bot.register_next_step_handler(msg, receive_photo)

def receive_photo(message):
    if message.photo:
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        if not os.path.exists('photos'):
            os.makedirs('photos')

        with open(f'photos/{message.photo[-1].file_id}.jpg', 'wb') as new_file:
            new_file.write(downloaded_file)

        msg = bot.send_message(message.chat.id, 'Фото получено. Теперь отправьте описание:')
        bot.register_next_step_handler(msg, lambda m: receive_description(m, message.photo[-1].file_id))
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, отправьте фото.')

def receive_description(message, photo_file_id):
    description = message.text
    if description:
        broadcast_message(photo_file_id, description)
        bot.send_message(message.chat.id, 'Сообщение отправлено всем пользователям.')
    else:
        bot.send_message(message.chat.id, 'Описание не может быть пустым.')

def broadcast_message(photo_file_id, description):
    conn = sqlite3.connect('tinkoffBot.sql')
    cur = conn.cursor()

    cur.execute('SELECT name FROM users WHERE subs = 1')
    user_ids = cur.fetchall()

    photo_path = f'photos/{photo_file_id}.jpg'
    with open(photo_path, 'rb') as photo:
        for user_id in user_ids:
            try:
                bot.send_photo(user_id[0], photo, caption=description)
                photo.seek(0)
            except Exception as e:
                print(f'Ошибка при отправке сообщения пользователю {user_id[0]}: {e}')

    cur.close()
    conn.close()

    # Удаление фото после отправки
    if os.path.exists(photo_path):
        os.remove(photo_path)


@bot.message_handler(commands=['settings'])
def settings(message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('Подписаться', callback_data='subscribe'))
    keyboard.add(types.InlineKeyboardButton('Отписаться', callback_data='unsubscribe'))
    bot.send_message(message.chat.id, 'Подписаться на рассылки?', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def handle_subscription(call):
    conn = sqlite3.connect('tinkoffBot.sql')
    cur = conn.cursor()
    try:
        if call.data == 'subscribe':
            cur.execute('UPDATE users SET subs = 1 WHERE name = ?', (call.message.chat.id,))
            bot.send_message(call.message.chat.id, 'Вы подписались на рассылки.')
        elif call.data == 'unsubscribe':
            cur.execute('UPDATE users SET subs = 0 WHERE name = ?', (call.message.chat.id,))
            bot.send_message(call.message.chat.id, 'Вы отписались от рассылки.')
        conn.commit()
    except Exception as e:
        bot.send_message(call.message.chat.id, 'Произошла ошибка: ' + str(e))
    finally:
        cur.close()
        conn.close()

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if call.data == 'subscribe':
        cur.execute('UPDATE users SET subs = 1 WHERE name = ?', (call.message.chat.id,))
        bot.send_message(call.message.chat.id, 'Вы подписались на рассылки.')
        conn.commit()

    elif call.data == 'unsubscribe':
        cur.execute('UPDATE users SET subs = 0 WHERE name = ?', (call.message.chat.id,))
        bot.send_message(call.message.chat.id, 'Вы отписались от рассылки.')
        conn.commit()

    cur.close()
    conn.close()



@bot.message_handler(content_types=['text'])
def text(message):
    question = message.text
    if len(question) >= 6:
        body = {
            "query": message.text
        }
        response = requests.post("http://127.0.0.1:5000/assist", json=body)
        if response.status_code == 200:
            reply = response.text
            # Проверяем длину ответа и разбиваем его, если необходимо
            max_length = 4096
            for i in range(0, len(reply), max_length):
                bot.send_message(message.chat.id, reply[i:i + max_length])
        else:
            bot.send_message(message.chat.id, 'Ошибка при запросе к серверу.')
    else:
        bot.send_message(message.chat.id, "Слишком маленький запрос.")

if __name__ == '__main__':
    print("Bot started")
    bot.polling(none_stop=True)

    
