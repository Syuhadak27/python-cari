import time
import re
import threading  # Tambahkan ini untuk menggunakan threading
from telebot import TeleBot
from Button import create_refresh_button
from pesan import KURANG_KATA, TIDAK_ADA, RESPON_TEXT
from delete import schedule_deletion, delete_message_safe
from cache import get_google_sheet_data, cached_main_data,cached_list_data,reset_cache,  cache_timestamps, CACHE_EXPIRY

def handle_refresh(bot, message):
    global cached_inout_data, cached_stok_data, cached_main_data,cached_list_data, cache_timestamps
    cached_inout_data = None
    cached_stok_data = None
    cached_main_data = None
    cached_list_data = None
    cache_timestamps = {
        "inout": 0,
        "stok": 0,
        "main": 0,
        "list": 0
    }
    msg = bot.reply_to(message, "Data telah di perbarui, coba ulangi kata kunci nya lagi🥰")
    schedule_deletion(bot, message.chat.id, msg.message_id, 1)
    schedule_deletion(bot, message.chat.id, message.message_id, 1)

def schedule_deletion(bot, chat_id, message_id, delay):
    threading.Timer(delay, lambda: delete_message_safe(bot, chat_id, message_id)).start()

#def delete_message_safe(bot, chat_id, message_id):
 #   try:
 #       bot.delete_message(chat_id, message_id)
#    except Exception as e:
  #      pass


def handle_message(bot, message, SPREADSHEET_ID, RANGE_NAME):
    global cached_main_data
    query = message.text

    query_parts = query.split()

    if cached_main_data is None or time.time() - cache_timestamps["main"] > CACHE_EXPIRY:
        cached_main_data = get_google_sheet_data(SPREADSHEET_ID, RANGE_NAME)
        cache_timestamps["main"] = time.time()

    filtered_data = [row for row in cached_main_data if all(re.search(re.escape(part), ' '.join(row), re.IGNORECASE) for part in query_parts)]
    
    #response = RESPON_TEXT
    #response = f"{RESPON_TEXT} • • <i>Kata Kunci</i> : <b>{query}</b>\n\n"
    response = f"{RESPON_TEXT} • • <i>Kata Kunci</i> : <code>. {query}</code>\n\n"
    if filtered_data:
        for row in filtered_data:
            formatted_row = [f"<code>{col}</code>" if i == 1 else col for i, col in enumerate(row)]
            response += "➡️ " + ' • '.join(formatted_row) + "\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
        schedule_deletion(bot, message.chat.id, message.message_id, 2)
    else:
        response = TIDAK_ADA
        msg = bot.send_message(message.chat.id, response, reply_markup=create_refresh_button(), parse_mode="HTML")
        schedule_deletion(bot, message.chat.id, msg.message_id, 7)
        schedule_deletion(bot, message.chat.id, message.message_id, 2)
        return

    def send_long_message(chat_id, message_text):
        max_length = 4096
        # Memastikan pesan tidak terpotong di tengah tag HTML
        while message_text:
            part = message_text[:max_length]
            if len(part) == max_length:
                last_index = part.rfind("</code>") + len("</code>")
                if last_index > 0:
                    part = message_text[:last_index]
                else:
                    part = message_text[:max_length]
            bot.send_message(chat_id, part, parse_mode="HTML")
            message_text = message_text[len(part):]

    send_long_message(message.chat.id, response)