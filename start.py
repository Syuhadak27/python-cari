import re
import time
import threading
from telebot import TeleBot
from Button import create_refresh_button,tombol_ganda, delete_button
from delete import schedule_deletion
from pesan import PESAN_HELP

def handle_start(bot, message):
    msg = bot.reply_to(
        message, 
        "Bot aktif🟢🟢🟢⚪⚪ \n\n<b>Bot ini menggunakan cache agar lebih responsive</b>, \n\n<code>Tekan tombol di bawah untuk merefresh cache🥰🥰</code>",
        parse_mode="HTML",
        reply_markup=tombol_ganda()
    )
    schedule_deletion(bot, message.chat.id, msg.message_id, 9)
    
def handle_help(bot, message):
    msg = bot.reply_to(
        message, PESAN_HELP,
        parse_mode="HTML",)
    schedule_deletion(bot, message.chat.id, message.message_id, 2)
    schedule_deletion(bot, message.chat.id, msg.message_id, 7)