from app.services import BDService
from app.config import Config
import telebot

config = Config()
service = BDService()
bot = telebot.TeleBot(config["bot"]["api"])
