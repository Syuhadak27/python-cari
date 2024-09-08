import re
import time
import threading
from telebot import TeleBot
from Button import create_refresh_button
from pesan import KURANG_KATA, TIDAK_ADA, RESPON_TEXT
from cache import get_google_sheet_data, cached_inout_data, cached_stok_data, cache_timestamps, CACHE_EXPIRY,cached_list_data
from delete import schedule_deletion

def handle_stok(bot, message, SPREADSHEET_ID, RANGE_STOK):
    global cached_stok_data
    query = message.text.split(' ', 1)[1] if len(message.text.split(' ', 1)) > 1 else ''
    
    if not query:
        msg = bot.reply_to(message, KURANG_KATA)
        schedule_deletion(bot, message.chat.id, msg.message_id, 1)
        schedule_deletion(bot, message.chat.id, message.message_id, 1)
        return
    
    query_parts = query.split()

    if cached_stok_data is None or time.time() - cache_timestamps["stok"] > CACHE_EXPIRY:
        cached_stok_data = get_google_sheet_data(SPREADSHEET_ID, RANGE_STOK)
        cache_timestamps["stok"] = time.time()

    filtered_data = [row for row in cached_stok_data if all(re.search(re.escape(part), ' '.join(row), re.IGNORECASE) for part in query_parts)]

    #response = f"{RESPON_TEXT}\n"
    response = f"{RESPON_TEXT}••Kata Kunci : {query}\n\n"
    if filtered_data:
        for row in filtered_data:
            response += "➡️" + ' • '.join(row) + "\n"
        schedule_deletion(bot, message.chat.id, message.message_id, 2)
    else:
        response = TIDAK_ADA
        msg = bot.send_message(message.chat.id, response, reply_markup=create_refresh_button())
        schedule_deletion(bot, message.chat.id, msg.message_id, 2)
        schedule_deletion(bot, message.chat.id, message.message_id, 2)
        return

    def send_long_message(chat_id, message_text):
        max_length = 4096
        for i in range(0, len(message_text), max_length):
            bot.send_message(chat_id, message_text[i:i+max_length])

    send_long_message(message.chat.id, response)