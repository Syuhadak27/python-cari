import telebot
from config import BOT_TOKEN, SPREADSHEET_ID, RANGE_NAME
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from stok import handle_stok
from inout import handle_inout
from start import handle_help, handle_start
from list import handle_list
from delete import schedule_deletion
from master import handle_refresh, handle_message
import threading
import time

bot = telebot.TeleBot(BOT_TOKEN)

# Konfigurasi Google Sheets API
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
creds = Credentials.from_service_account_file('baca-id.json', scopes=SCOPES)
service = build('sheets', 'v4', credentials=creds)

# Fungsi untuk mendapatkan ID admin dari sheet
def get_admin_ids():
    sheet = service.spreadsheets()
    try:
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range='USERID!A2').execute()
        values = result.get('values', [])
        admin_ids = [int(row[0]) for row in values] if values else []
        print(f"ID Admin Ditemukan: {admin_ids}")  # Debugging: Tampilkan ID admin yang ditemukan
        return admin_ids
    except Exception as e:
        print(f"Terjadi kesalahan saat mengambil ID admin: {e}")
        return []

# Fungsi untuk mendapatkan user ID yang diizinkan
def get_allowed_user_ids():
    sheet = service.spreadsheets()
    try:
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range='USERID!A2:A').execute()
        values = result.get('values', [])
        ids = [int(row[0]) for row in values] if values else []
        print(f"ID Pengguna Ditemukan: {ids}")  # Debugging: Tampilkan ID yang ditemukan
        return ids
    except Exception as e:
        print(f"Terjadi kesalahan saat mengambil user ID: {e}")
        return []

# Variabel global untuk menyimpan ID pengguna dan admin
allowed_user_ids = get_allowed_user_ids()
admin_ids = get_admin_ids()

# Fungsi untuk memperbarui ID pengguna dan admin secara berkala
def update_ids_periodically(interval=3600):
    global allowed_user_ids, admin_ids
    while True:
        allowed_user_ids = get_allowed_user_ids()
        admin_ids = get_admin_ids()
        print(f"User ID diperbarui: {allowed_user_ids}")  # Debugging: Tampilkan ID pengguna yang diperbarui
        print(f"Admin ID diperbarui: {admin_ids}")  # Debugging: Tampilkan ID admin yang diperbarui
        time.sleep(interval)

# Mulai thread untuk pembaharuan berkala
threading.Thread(target=update_ids_periodically, daemon=True).start()

# Fungsi untuk memperbarui ID pengguna secara manual
def refresh_user_ids(message):
    global allowed_user_ids
    allowed_user_ids = get_allowed_user_ids()
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
        if message.from_user.id in allowed_user_ids:
            return func(message)
        else:
            bot.send_message(message.chat.id, "Akses ditolak.")
    return wrapper

@bot.message_handler(commands=['refresh_id'])
@admin_only
def handle_refresh_id(message):
    refresh_user_ids(message)

@bot.callback_query_handler(func=lambda call: call.data == 'delete')
@restrict_access
def handle_delete_callback(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    schedule_deletion(bot, chat_id, message_id)

@bot.message_handler(commands=['start'])
@restrict_access
def send_welcome(message):
    handle_start(bot, message)

@bot.message_handler(commands=['help'])
@restrict_access
def send_help(message):
    handle_help(bot, message)

@bot.callback_query_handler(func=lambda call: call.data == 'help')
@restrict_access
def callback_help(call):
    handle_help(bot, call.message)

@bot.callback_query_handler(func=lambda call: call.data == 'refresh')
@restrict_access
def callback_refresh(call):
    handle_refresh(bot, call.message)

@bot.message_handler(commands=['refresh'])
@restrict_access
def refresh_cache(message):
    handle_refresh(bot, message)

@bot.message_handler(func=lambda message: message.text.startswith(('. ', '/inout')))
@restrict_access
def inout_handler(message):
    handle_inout(bot, message)

@bot.message_handler(func=lambda message: message.text.startswith(('.stok ', '/stok')))
@restrict_access
def stok(message):
    handle_stok(bot, message)

@bot.message_handler(func=lambda message: message.text.startswith(('.list ', '/list')))
@restrict_access
def list(message):
    handle_list(bot, message)

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