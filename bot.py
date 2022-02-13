from sre_compile import isstring
import textwrap
import telebot
import settings
from telebot import types
import psycopg2
from psycopg2 import Error

bot = telebot.TeleBot(settings.TOKEN)

def search_goods_db(message):
    try:
        conn = psycopg2.connect(
            user='postgres',
            password = '5432',
            host = 'localhost',
            port= '5432',
            database = 'postgres'
        )
        cursor = conn.cursor()
        cursor.execute(f"""select * from goods where code='{message.text}'""")
        record = cursor.fetchall()
        print(record[0])
        text = ''
        for i in record[0]:
            if isinstance(i,str):
                text = text + ' ' + i
        
        bot.send_message(message.chat.id,text)
                
        
        record = cursor.fetchone()
        print('version',record)
    except (Exception, Error) as error:
        print('error', error)
    finally:
        if conn:
            cursor.close()
            conn.close()
            print('Conn close')

def add_goods_db(message):
    item = message.text.split(' ')
    if(len(item) == 4):
        try:
            conn = psycopg2.connect(
                user='postgres',
                password='5432',
                host='localhost',
                port='5432',
                database='postgres'
            )
            cursor = conn.cursor()
            add_query  =f"""insert into goods (code, name,color,location) values (
                '{item[0]}','{item[1]}','{item[2]}','{item[3]}')"""
            cursor.execute(add_query)
            conn.commit()

        except(Exception, Error) as error:
            bot.send_message(message.chat.id, 'error ', error)
        finally:
            cursor.close()
            conn.close()
            print('Conn close')
    else:
        bot.send_message(message.chat.id,'Не правильный формат')


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Welcome!')
    actions(message)

def actions(message):
    markup = types.InlineKeyboardMarkup()
    search_goods = types.InlineKeyboardButton(text="Поиск товара",callback_data="search_goods")
    add_goods = types.InlineKeyboardButton(text="Добавление товара", callback_data="add_goods")
    delete_goods = types.InlineKeyboardButton(text="Удаление товара",callback_data="delete_goods")
    markup.add(search_goods,add_goods,delete_goods)
    bot.send_message(message.chat.id,'Что вы хотите!?',reply_markup=markup)



@bot.callback_query_handler(func=lambda call:True)
def query_handler(call):
    if(call.data == "search_goods"):
        sent = bot.send_message(call.message.chat.id, 'Код товара?')
        bot.register_next_step_handler(sent,search_goods_db)
    elif(call.data == "add_goods"):
        sent = bot.send_message(call.message.chat.id, 'Код Имя Цвет Локация')
        bot.register_next_step_handler(sent,add_goods_db)


bot.infinity_polling()
