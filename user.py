from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
import time
import telebot

# Konfigurasi Google Sheets API
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = Credentials.from_service_account_file('baca-id.json', scopes=SCOPES)
service = build('sheets', 'v4', credentials=creds)

def get_admin_ids(spreadsheet_id):
    """
    Mengambil ID admin dari sheet.
    
    Args:
    - spreadsheet_id: ID spreadsheet Google Sheets
    
    Returns:
    - Daftar ID admin
    """
    sheet = service.spreadsheets()
    try:
        result = sheet.values().get(spreadsheetId=spreadsheet_id, range='USERID!A2').execute()
        values = result.get('values', [])
        admin_ids = [int(row[0]) for row in values] if values else []
        print(f"ID Admin Ditemukan: {admin_ids}")  # Debugging: Tampilkan ID admin yang ditemukan
        return admin_ids
    except Exception as e:
        print(f"Terjadi kesalahan saat mengambil ID admin: {e}")
        return []

def get_allowed_user_ids(spreadsheet_id):
    """
    Mengambil user ID yang diizinkan dari sheet.
    
    Args:
    - spreadsheet_id: ID spreadsheet Google Sheets
    
    Returns:
    - Daftar user ID yang diizinkan
    """
    sheet = service.spreadsheets()
    try:
        result = sheet.values().get(spreadsheetId=spreadsheet_id, range='USERID!A2:A').execute()
        values = result.get('values', [])
        ids = [int(row[0]) for row in values] if values else []
        print(f"ID Pengguna Ditemukan: {ids}")  # Debugging: Tampilkan ID yang ditemukan
        return ids
    except Exception as e:
        print(f"Terjadi kesalahan saat mengambil user ID: {e}")
        return []

def update_ids_periodically(spreadsheet_id, interval=3600):
    """
    Memperbarui ID pengguna dan admin secara berkala.
    
    Args:
    - spreadsheet_id: ID spreadsheet Google Sheets
    - interval: Interval waktu dalam detik
    """
    global allowed_user_ids, admin_ids
    while True:
        allowed_user_ids = get_allowed_user_ids(spreadsheet_id)
        admin_ids = get_admin_ids(spreadsheet_id)
        print(f"User ID diperbarui: {allowed_user_ids}")  # Debugging: Tampilkan ID pengguna yang diperbarui
        print(f"Admin ID diperbarui: {admin_ids}")  # Debugging: Tampilkan ID admin yang diperbarui
        time.sleep(interval)

def add_user_id(user_id, spreadsheet_id):
    """
    Menambahkan ID pengguna yang diterima ke sheet.
    
    Args:
    - user_id: ID pengguna yang akan ditambahkan
    - spreadsheet_id: ID spreadsheet Google Sheets
    """
    sheet = service.spreadsheets()
    try:
        # Mendapatkan range untuk baris kosong berikutnya
        result = sheet.values().get(spreadsheetId=spreadsheet_id, range='USERID!A:A').execute()
        values = result.get('values', [])
        next_row = len(values) + 1
        
        range_name = f'USERID!A{next_row}'
        body = {
            'values': [[user_id]]
        }
        sheet.values().update(spreadsheetId=spreadsheet_id, range=range_name,
                              valueInputOption='RAW', body=body).execute()
        print(f"ID {user_id} ditambahkan ke baris {next_row}.")
    except Exception as e:
        print(f"Terjadi kesalahan saat menambahkan ID pengguna: {e}")

def send_access_denied_message(bot, message, user_id, admin_ids):
    """
    Mengirimkan pesan akses ditolak kepada pengguna yang tidak terdaftar.
    
    Args:
    - bot: Instance dari bot Telegram
    - message: Pesan Telegram yang diterima
    - user_id: ID pengguna yang tidak terdaftar
    - admin_ids: Daftar ID admin yang dapat menerima laporan
    """
    access_denied_message = (
        f"Anda tidak terdaftar sebagai anggota bot ini. "
        f"Kirimkan ID ini {user_id} ke admin."
    )
    markup = telebot.types.InlineKeyboardMarkup()
    send_id_button = telebot.types.InlineKeyboardButton("Kirim ID ke Admin", callback_data=f'send_id_{user_id}')
    markup.add(send_id_button)
    bot.send_message(message.chat.id, access_denied_message, reply_markup=markup)
    for admin_id in admin_ids:
        bot.send_message(admin_id, f"Pengguna dengan ID {user_id} mencoba mengakses bot tetapi tidak terdaftar.")

def handle_send_id_callback(bot, call):
    """
    Menangani callback dari tombol "Kirim ID ke Admin".
    
    Args:
    - bot: Instance dari bot Telegram
    - call: Callback dari tombol
    """
    user_id = int(call.data.split('_')[-1])
    admin_ids = get_admin_ids(SPREADSHEET_ID)
    for admin_id in admin_ids:
        bot.send_message(admin_id, f"Pengguna dengan ID {user_id} meminta akses. ID mereka adalah {user_id}.")
    bot.delete_message(call.message.chat.id, call.message.message_id)  # Hapus pesan permintaan akses

def handle_accept_user_callback(bot, call):
    """
    Menangani callback dari tombol "Terima" yang ditekan oleh admin.
    
    Args:
    - bot: Instance dari bot Telegram
    - call: Callback dari tombol
    """
    user_id = int(call.data.split('_')[-1])
    if call.from_user.id in admin_ids:
        # ID pengguna diterima dan ditambahkan ke sheet
        add_user_id(user_id, SPREADSHEET_ID)
        bot.send_message(call.message.chat.id, f"ID {user_id} telah diterima dan ditambahkan.")
        bot.send_message(user_id, "Akses Anda telah diberikan.")
    else:
        bot.send_message(call.message.chat.id, "Hanya admin yang dapat melakukan tindakan ini.")
    bot.delete_message(call.message.chat.id, call.message.message_id)  # Hapus pesan permintaan akses