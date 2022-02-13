import telebot
import settings
from telebot import types
bot = telebot.TeleBot(settings.TOKEN)

bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Welcome!')
    bot.send_message(message.chat.id, 'Click, /action')
    actions(message)

def actions(message):
    markup = types.InlineKeyboardMarkup()
    search_goods = types.InlineKeyboardButton(text="Поиск товара",callback_data="search_goods")
    add_goods = types.InlineKeyboardButton(text="Добавление товара", callback_data="add_goods")
    delete_goods = types.InlineKeyboardButton(text="Удаление товара",callback_data="delete_goods")
    markup.add(search_goods,add_goods,delete_goods)

    bot.send_message(message.chat.id,'Что вы хотите!?',reply_markup=markup)


bot.infinity_polling()