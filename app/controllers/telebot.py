from venv import create

from app.services import BDService
from app.config import Config
import telebot
from telebot import types

config = Config()
service = BDService()
bot = telebot.TeleBot(config["bot"]["api"])

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "/start":
        bot.send_message(message.from_user.id, 'По какому параметру найти комету?' ,reply_markup=keyboard)
    elif message.text == "/admin":
        bot.send_message(message.from_user.id, 'Что вы хотите сделать?' ,reply_markup=keyboard1)
    else:
        bot.send_message(message.from_user.id, "Напиши /start")


keyboard = types.InlineKeyboardMarkup()
key_random = types.InlineKeyboardButton(text='Случайно', callback_data='random')
keyboard.add(key_random)
key_diameter = types.InlineKeyboardButton(text='По диаметру', callback_data='diameter')
keyboard.add(key_diameter)
key_name = types.InlineKeyboardButton(text='По названию', callback_data='name')
keyboard.add(key_name)
key_id = types.InlineKeyboardButton(text='По ID', callback_data='id')
keyboard.add(key_id)

keyboard1 = types.InlineKeyboardMarkup()
key_find = types.InlineKeyboardButton(text='Найти', callback_data='keyboard')
keyboard1.add(key_find)
key_delete = types.InlineKeyboardButton(text='Удалить', callback_data='delete')
keyboard1.add(key_delete)
key_change = types.InlineKeyboardButton(text='Изменить', callback_data='change')
keyboard1.add(key_change)
key_create = types.InlineKeyboardButton(text='Создать', callback_data='create')
keyboard1.add(key_create)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "random":
        bot.send_message(call.message.chat.id, 'Функция пока в разработке.')
    elif call.data == "diameter":
        bot.send_message(call.message.chat.id, 'Напиши диаметр')
        bot.register_next_step_handler(message, service.get_comet_by_diameter())
    elif call.data == "name":
        bot.send_message(call.message.chat.id, 'Напиши имя')
        bot.register_next_step_handler(message, service.get_comet_by_name())
    elif call.data == "id":
        bot.send_message(call.message.chat.id, 'Напиши ID')
        bot.register_next_step_handler(message, service.get_comet_by_id())
    elif call.data == "delete":
        bot.send_message(call.message.chat.id, '')
        bot.register_next_step_handler(message, service.get_comet_by_id())
    elif call.data == "change":
        bot.send_message(call.message.chat.id, '')
        bot.register_next_step_handler(message, service.get_comet_by_id())
    elif call.data == "create":
        bot.send_message(call.message.chat.id, '')
        bot.register_next_step_handler(message, service.create())
    elif call.data == "keyboard":
        bot.send_message(call.message.chat.id, 'Напиши /start')