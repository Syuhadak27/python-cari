import time
import re
import time
import threading
from telebot import TeleBot
from Button import create_refresh_button


def schedule_deletion(bot, chat_id, message_id, delay):
    threading.Timer(delay, lambda: delete_message_safe(bot, chat_id, message_id)).start()

def delete_message_safe(bot, chat_id, message_id):
    try:
        bot.delete_message(chat_id, message_id)
    except Exception as e:
        pass