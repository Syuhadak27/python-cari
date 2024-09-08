import re
import time
import threading
from telebot import TeleBot
from Button import create_refresh_button
from delete import schedule_deletion
from cache import get_google_sheet_data, cached_inout_data, cache_timestamps, CACHE_EXPIRY

def handle_inout(bot, message, INOUT_ID, RANGE_INOUT):
    global cached_inout_data
    query = message.text[1:]  # Menghapus titik di awal

    if not query:
        msg = bot.reply_to(message, "Tidak bisa tanpa kata kunci")
        schedule_deletion(bot, message.chat.id, msg.message_id, 2)
        schedule_deletion(bot, message.chat.id, message.message_id, 2)
        return

    query_parts = query.split()

    if cached_inout_data is None or time.time() - cache_timestamps["inout"] > CACHE_EXPIRY:
        cached_inout_data = get_google_sheet_data(INOUT_ID, RANGE_INOUT)
        cache_timestamps["inout"] = time.time()

    filtered_data = [
        row for row in cached_inout_data 
        if all(re.search(re.escape(part), ' '.join(row), re.IGNORECASE) for part in query_parts)
    ]

    response = f"Kata Kunci: <code>{query}</code>\nKet:\n🟢 Masuk \n🔴 <b>Keluar</b>\n\n"
    
    if filtered_data:
        for row in filtered_data:
            # Format kolom pertama dengan <pre><code> agar bisa di-copy dengan sekali klik
            response += f"🔄<code>{row[0]}</code> • " + ' • '.join(row[1:]) + "\n"
        schedule_deletion(bot, message.chat.id, message.message_id, 2)
    else:
        response = "Salah kata kunci dan tidak ditemukan😜\n\nUntuk memperbarui data tekan tombol di bawah."
        msg = bot.send_message(message.chat.id, response, reply_markup=create_refresh_button(), parse_mode='HTML')
        schedule_deletion(bot, message.chat.id, msg.message_id, 2)
        schedule_deletion(bot, message.chat.id, message.message_id, 2)
        return

    def send_long_message(chat_id, message_text):
        max_length = 4096
        for i in range(0, len(message_text), max_length):
            bot.send_message(chat_id, message_text[i:i+max_length], parse_mode='HTML')

    send_long_message(message.chat.id, response)