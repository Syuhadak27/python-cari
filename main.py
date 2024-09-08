import telebot
from user import get_admin_ids, get_allowed_user_ids, update_ids_periodically, send_access_denied_message, handle_send_id_callback, handle_accept_user_callback
import threading
from config import BOT_TOKEN, SPREADSHEET_ID, INOUT_ID, RANGE_NAME, RANGE_INOUT, RANGE_STOK, LIST_ID, RANGE_LIST
from stok import handle_stok
from inout import handle_inout
from start import handle_help, handle_start
from list import handle_list
from delete import schedule_deletion
from master import handle_refresh, handle_message

bot = telebot.TeleBot(BOT_TOKEN)

# Variabel global untuk menyimpan ID pengguna dan admin
allowed_user_ids = get_allowed_user_ids(SPREADSHEET_ID)
admin_ids = get_admin_ids(SPREADSHEET_ID)

# Mulai thread untuk pembaharuan berkala
threading.Thread(target=update_ids_periodically, args=(SPREADSHEET_ID,), daemon=True).start()

# Fungsi untuk memperbarui ID pengguna secara manual
def refresh_user_ids(message):
    global allowed_user_ids
    allowed_user_ids = get_allowed_user_ids(SPREADSHEET_ID)
    bot.send_message(message.chat.id, "User ID diperbarui secara manual.")
    print(f"User ID diperbarui secara manual: {allowed_user_ids}")  # Debugging: Tampilkan ID yang diperbarui

# Dekorator untuk memeriksa akses admin
def admin_only(func):
    def wrapper(message):
        if message.from_user.id in admin_ids:
            return func(message)
        else:
            bot.send_message(message.chat.id, "Akses admin diperlukan.")
    return wrapper

# Dekorator untuk memeriksa akses pengguna
def restrict_access(func):
    def wrapper(message):
        user_id = message.from_user.id
        if user_id in allowed_user_ids:
            return func(message)
        else:
            send_access_denied_message(bot, message, user_id, admin_ids)
    return wrapper

@bot.message_handler(commands=['refresh_id'])
@admin_only
def handle_refresh_id(message):
    refresh_user_ids(message)

@bot.callback_query_handler(func=lambda call: call.data.startswith('send_id_'))
def handle_send_id_callback_wrapper(call):
    handle_send_id_callback(bot, call)

@bot.callback_query_handler(func=lambda call: call.data.startswith('accept_user_'))
def handle_accept_user_callback_wrapper(call):
    handle_accept_user_callback(bot, call)

@bot.callback_query_handler(func=lambda call: call.data == 'delete')
def handle_delete_callback(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    schedule_deletion(bot, chat_id, message_id)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    handle_start(bot, message)

@bot.message_handler(commands=['help'])
def send_help(message):
    handle_help(bot, message)

@bot.callback_query_handler(func=lambda call: call.data == 'help')
def callback_help(call):
    handle_help(bot, call.message)

@bot.callback_query_handler(func=lambda call: call.data == 'refresh')
def callback_refresh(call):
    handle_refresh(bot, call.message)

@bot.message_handler(commands=['refresh'])
def refresh_cache(message):
    handle_refresh(bot, message)

@bot.message_handler(func=lambda message: message.text.startswith(('. ', '/inout')))
def inout_handler(message):
    handle_inout(bot, message, INOUT_ID, RANGE_INOUT)

@bot.message_handler(func=lambda message: message.text.startswith(('.stok ', '/stok')))
def stok(message):
    handle_stok(bot, message, SPREADSHEET_ID, RANGE_STOK)

@bot.message_handler(func=lambda message: message.text.startswith(('.list ', '/list')))
def list(message):
    handle_list(bot, message, LIST_ID, RANGE_LIST)

@bot.message_handler(func=lambda message: True)
@restrict_access
def message_handler(message):
    handle_message(bot, message, SPREADSHEET_ID, RANGE_NAME)

if __name__ == "__main__":
    print("Bot berjalan 🔴🔴🔴⚪⚪")
    try:
        bot.polling(non_stop=True)
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")