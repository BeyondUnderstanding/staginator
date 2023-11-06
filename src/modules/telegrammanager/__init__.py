from telebot import TeleBot
from config import TG_TOKEN, TG_CHAT_ID, TG_THREAD_ID
from .NotificationManager import NotificationManager

telegram = TeleBot(token=TG_TOKEN)
manager = NotificationManager(telegram, TG_CHAT_ID, TG_THREAD_ID)