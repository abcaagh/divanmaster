import psycopg2
from psycopg2 import Error
import telebot
import settings

bot = telebot.TeleBot(settings.TOKEN)


def db():
    record = None
    try:
        conn = psycopg2.connect(user='postgres',
                                password='5432',
                                host='localhost',
                                port='5432',
                                database='divan')
        cursor = conn.cursor()
        cursor.execute('SELECT version()')
        record =  cursor.fetchall()
    except (Exception, Error) as error:
        print('Error', error)
    finally:
        if conn:
            cursor.close()
            conn.close()
            print('Connection close')
    return record

@bot.message_handler(commands=['start'])
def start(message):
    print('bot started')
    record = db()
    print('bot db')
    print('rec',record)
    print('bot reply db')
    bot.send_message(message.chat.id,'Производитель')

bot.polling(none_stop=True)