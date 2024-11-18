from app.services import BDService
from app.models import *
from app.config import Config
import telebot
from telebot import types

config = Config()
service = BDService()
bot = telebot.TeleBot(config["bot"]["api"])

find_keyboard = types.InlineKeyboardMarkup([[
    types.InlineKeyboardButton(text="По ID", callback_data="id"),
    types.InlineKeyboardButton(text="По названию", callback_data="name"),
    types.InlineKeyboardButton(text="По диаметру", callback_data="diameter"),
    types.InlineKeyboardButton(text="Случайно", callback_data="random"),
]])

action_keyboard = types.InlineKeyboardMarkup([[
    types.InlineKeyboardButton(text="Найти", callback_data="keyboard"),
    types.InlineKeyboardButton(text="Удалить", callback_data="delete"),
    types.InlineKeyboardButton(text="Изменить", callback_data="update"),
    types.InlineKeyboardButton(text="Создать", callback_data="create")
]])


@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == "/start":
        bot.send_message(message.from_user.id, "По какому параметру найти комету?", reply_markup=find_keyboard)
    elif message.text == "/admin":
        bot.send_message(message.from_user.id, "Введите пароль:", reply_markup=action_keyboard)
        bot.register_next_step_handler(message, auth)
    else:
        bot.send_message(message.from_user.id, "Напиши /start")


"""USER"""


@bot.callback_query_handler(func=lambda call: True)
def find_comet(call):
    match call.data:
        case "random":
            comet = service.get_random_comet()
            bot.send_message(call.message.chat.id, str(comet))
        case "diameter":
            bot.send_message(call.message.chat.id, "Напиши диаметр")
            bot.register_next_step_handler(call.message, get_by_diameter)
        case "name":
            bot.send_message(call.message.chat.id, "Напиши имя")
            bot.register_next_step_handler(call.message, get_by_name)
        case "id":
            bot.send_message(call.message.chat.id, "Напиши ID")
            bot.register_next_step_handler(call.message, get_by_id)


def get_by_diameter(message):
    try:
        comet = service.get_comet_by_diameter(message.text)
        bot.send_message(message.from_user.id, str(comet))
    except IndexError:
        bot.send_message(message.from_user.id, f"Нет кометы с диаметром: {message.text}")


def get_by_name(message):
    try:
        comet = service.get_comet_by_name(message.text)
        bot.send_message(message.from_user.id, str(comet))
    except IndexError:
        bot.send_message(message.from_user.id, f"Нет кометы с именем: {message.text}")


def get_by_id(message):
    try:
        comet = service.get_comet_by_id(message.text)
        bot.send_message(message.from_user.id, str(comet))
    except IndexError:
        bot.send_message(message.from_user.id, f"Нет кометы с id: {message.text}")


"""ADMIN"""


def auth(message):
    if message.text == config["bot"]["password"]:
        bot.send_message(message.message.chat.id, "Пароль не верный")
    else:
        bot.send_message(message.from_user.id, "Что вы хотите сделать?", reply_markup=action_keyboard)
        bot.register_next_step_handler(message, auth)


@bot.callback_query_handler(func=lambda call: True)
def get_admin(call):
    match call:
        case "delete":
            bot.send_message(call.message.chat.id, "Введи id кометы")
            bot.register_next_step_handler(call.message, delete)
        case "update":
            bot.send_message(call.message.chat.id, "Введи id кометы")
            bot.register_next_step_handler(call.message, find_to_update)
        case "create":
            bot.send_message(call.message.chat.id,
                             "Введи поля кометы через запятую: name, diameter, neo, albedo, period, class")
            bot.register_next_step_handler(call.message, create)
        case "keyboard":
            bot.send_message(call.message.chat.id, "Напиши /start")


def delete(message):
    try:
        service.delete_comet(message.text)
        bot.send_message(message.from_user.id, "Комета удалена")
    except IndexError:
        bot.send_message(message.from_user.id, f"Нет кометы с id: {message.text}")


def create(message):
    fields = message.text.split(", ")
    comet = fabric_comet_by_fields(fields)
    try:
        service.create_comet(comet)
        bot.send_message(message.from_user.id, "Комета создана")
    except IndexError:
        bot.send_message(message.from_user.id, "Не удалось создать комету")


def find_to_update(message):
    bot.send_message(message.message.chat.id,
                     "Введи поля кометы через запятую: name, diameter, neo, albedo, period, class")
    bot.register_next_step_handler(message, update)


def update(message):
    fields = message.text.split(", ")
    comet = fabric_comet_by_fields(fields)
    try:
        service.create_comet(comet)
        bot.send_message(message.from_user.id, "Комета обновленна")
    except IndexError:
        bot.send_message(message.from_user.id, "Не удалось обновить комету")
