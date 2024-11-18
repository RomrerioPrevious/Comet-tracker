from app.services import BDService
from app.models import *
from app.config import Config
import telebot
from telebot import types

config = Config()
service = BDService()
bot = telebot.TeleBot(config["bot"]["api"])

find_keyboard = types.InlineKeyboardMarkup([[
    types.InlineKeyboardButton(text="По ID", callback_data="get_id"),
    types.InlineKeyboardButton(text="По названию", callback_data="get_name"),
    types.InlineKeyboardButton(text="По диаметру", callback_data="get_diameter"),
    types.InlineKeyboardButton(text="Случайно", callback_data="get_random"),
]])

admin_keyboard = types.InlineKeyboardMarkup([[
    types.InlineKeyboardButton(text="Найти", callback_data="admin_get"),
    types.InlineKeyboardButton(text="Удалить", callback_data="admin_delete"),
    types.InlineKeyboardButton(text="Изменить", callback_data="admin_update"),
    types.InlineKeyboardButton(text="Создать", callback_data="admin_create")
]])

action_keyboard = types.InlineKeyboardMarkup([[
    types.InlineKeyboardButton(text="Найти комету", callback_data="action_get"),
    types.InlineKeyboardButton(text="Открыть админ панель", callback_data="action_admin")
]])


@bot.message_handler(content_types=["text"])
def start(message):
    if message.text == "/start":
        bot.send_message(message.from_user.id, "Что хотите сделать?", reply_markup=action_keyboard)


@bot.callback_query_handler(func=lambda call: call.data[0:6] == "action")
def start(call):
    match call.data:
        case "action_get":
            bot.send_message(call.message.chat.id, "По какому параметру найти комету?", reply_markup=find_keyboard)
        case "action_admin":
            bot.send_message(call.message.chat.id, "Введите пароль:")
            bot.register_next_step_handler(call.message, auth)


"""USER"""


@bot.callback_query_handler(func=lambda call: call.data[0:3] == "get")
def find_comet(call):
    match call.data:
        case "get_random":
            comet = service.get_random_comet()
            bot.send_message(call.message.chat.id, str(comet))
        case "get_diameter":
            bot.send_message(call.message.chat.id, "Напиши диаметр")
            bot.register_next_step_handler(call.message, get_by_diameter)
        case "get_name":
            bot.send_message(call.message.chat.id, "Напиши имя")
            bot.register_next_step_handler(call.message, get_by_name)
        case "get_id":
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
        bot.send_message(message.from_user.id, "Что вы хотите сделать?", reply_markup=admin_keyboard)
    else:
        bot.send_message(message.from_user.id, "Пароль не верный. Введите его повторно.")
        bot.register_next_step_handler(message, auth)


@bot.callback_query_handler(func=lambda call: call.data[0:5] == "admin")
def get_admin(call):
    match call.data:
        case "admin_delete":
            bot.send_message(call.message.chat.id, "Введи id кометы")
            bot.register_next_step_handler(call.message, delete)
        case "admin_update":
            bot.send_message(call.message.chat.id,
                             "Введи поля кометы через запятую: id, name, diameter, neo, albedo, period, class")
            bot.register_next_step_handler(call.message, update)
        case "admin_create":
            bot.send_message(call.message.chat.id,
                             "Введи поля кометы через запятую: name, diameter, neo, albedo, period, class")
            bot.register_next_step_handler(call.message, create)
        case "admin_get":
            bot.send_message(call.message.chat.id, "По какому параметру найти комету?", reply_markup=find_keyboard)


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


def update(message):
    fields = message.text.split(", ")
    comet = fabric_comet_by_fields(fields)
    try:
        service.update_comet(comet)
        bot.send_message(message.from_user.id, "Комета обновленна")
    except IndexError:
        bot.send_message(message.from_user.id, "Не удалось обновить комету")
