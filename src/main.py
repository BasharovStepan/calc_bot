import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import telebot
from telebot import types

import texts
from calculator import count_cal_norm
from config import *


# Telegram session
bot = telebot.TeleBot(telegram_key)


# Vars
user_states = {}
user_data = {}


# Keyboards
male_female_keyboard = types.InlineKeyboardMarkup()
btn1 = types.InlineKeyboardButton(text=texts.male, callback_data='male')
btn2 = types.InlineKeyboardButton(text=texts.female, callback_data='female')
male_female_keyboard.add(btn1, btn2)

activeness_cef_keyboard = types.InlineKeyboardMarkup()
cef12 = types.InlineKeyboardButton(text=texts.cef12, callback_data='cef12')
cef13 = types.InlineKeyboardButton(text=texts.cef13, callback_data='cef13')
cef15 = types.InlineKeyboardButton(text=texts.cef15, callback_data='cef15')
cef17 = types.InlineKeyboardButton(text=texts.cef17, callback_data='cef17')
activeness_cef_keyboard.add(cef12, cef13, cef15, cef17, row_width=1)


@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.from_user.id
    user_states[user_id] = 'weight'
#    bot.send_message(message.chat.id, texts.intro)
    bot.send_message(message.chat.id, texts.weight)


@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    user_id = message.from_user.id
    if user_id not in user_states:
        return

    current_state = user_states.get(user_id)

    try:
        float(message.text)

        if current_state == 'weight':
            user_data[user_id] = [int(message.text)]

            bot.send_message(user_id, texts.height)
            user_states[user_id] = 'height'


        elif current_state == 'height':
            user_data[user_id].append(int(message.text))

            bot.send_message(user_id, texts.age)
            user_states[user_id] = 'age'


        elif current_state == 'age':
            user_data[user_id].append(int(message.text))

            bot.send_message(user_id, texts.activeness_cef, reply_markup=activeness_cef_keyboard)
            user_states[user_id] = 'activeness_cef'


        elif current_state == 'activeness_cef':
            user_data[user_id].append(float(message.text))

            bot.send_message(user_id, texts.sex, reply_markup=male_female_keyboard)
            del user_states[user_id]

    except ValueError:
        user_states[user_id] = current_state
        bot.send_message(user_id, texts.not_a_number)



@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    user_id = call.message.chat.id

    bot.delete_message(call.message.chat.id, call.message.message_id)

    # Activeness coefficient
    if call.data in {'cef12', 'cef13', 'cef15', 'cef17'}:

        if call.data == 'cef12':
            user_data[user_id].append(1.2)
        if call.data == 'cef13':
            user_data[user_id].append(1.375)
        if call.data == 'cef15':
            user_data[user_id].append(1.550)
        if call.data == 'cef17':
            user_data[user_id].append(1.725)
        bot.send_message(user_id, texts.sex, reply_markup=male_female_keyboard)

    # Sex
    elif call.data in {'male', 'female'}:

        if call.data == 'male':
            user_data[user_id].append(True)
        elif call.data == 'female':
            user_data[user_id].append(False)

        args = user_data[user_id]

        # Calculate the result
        count = count_cal_norm(*args)
        bot.send_message(user_id, f"{count}")

if __name__ == '__main__':
    bot.polling(non_stop=True)
