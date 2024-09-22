import telebot
from telebot import types
import time

def wa_handler(bot, message):
    try:
        # Ambil nomor telepon dari teks setelah perintah /wa
        command, phone_number = message.text.split(maxsplit=1)

        # Validasi apakah nomor telepon hanya berupa angka
        if not phone_number.isdigit():
            error_message = bot.reply_to(message, 'Nomor telepon harus berupa angka.')
            time.sleep(3)
            bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)  # Hapus pesan pengguna
            bot.delete_message(chat_id=message.chat.id, message_id=error_message.message_id)  # Hapus pesan kesalahan
            return

        # Ganti angka 0 di depan nomor dengan 62
        if phone_number.startswith('0'):
            phone_number = '62' + phone_number[1:]

        # Buat tautan WhatsApp
        wa_link = f'https://wa.me/{phone_number}'

        # Buat tombol inline dengan tautan WhatsApp
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton(text=phone_number, url=wa_link)
        markup.add(btn)

        # Kirim pesan dengan tombol WhatsApp
        sent_message = bot.reply_to(message, "Klik tombol di bawah untuk menghubungi via WhatsApp", reply_markup=markup)

        # Hapus pesan pengguna setelah 3 detik
        time.sleep(3)
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)  # Hapus pesan pengguna
        #bot.delete_message(chat_id=message.chat.id, message_id=sent_message.message_id)  # Hapus pesan dengan tombol

    except ValueError:
        error_message = bot.reply_to(message, 'Silakan masukkan nomor telepon setelah /wa.')
        time.sleep(3)
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)  # Hapus pesan pengguna
        bot.delete_message(chat_id=message.chat.id, message_id=error_message.message_id)  # Hapus pesan kesalahan