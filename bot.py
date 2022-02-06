import telebot
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import settings
from telebot import types
bot = telebot.TeleBot(settings.TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton('ZD',callback_data='ZD'),
        types.InlineKeyboardButton('HC',callback_data='HC')
        )
    bot.send_message(message.chat.id,'Производитель',reply_markup=markup)

@bot.callback_query_handler(func=lambda call:True)
def manufacturer(call):
    if(call.data == 'ZD'):
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton('ZD-176-18G',callback_data='17618'),
            types.InlineKeyboardButton('ZD-176-19C',callback_data='17619')
            )
        bot.send_message(call.message.chat.id,'Код товара',reply_markup=markup)   
    
    ## adress

    elif(call.data == '17618'):
        bot.send_message(call.message.chat.id,'A1-3-1,В наличии 30 штукы')


bot.polling(none_stop=True)