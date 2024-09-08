import telebot

def delete_message_safe(bot, chat_id, message_id):
    try:
        bot.delete_message(chat_id=chat_id, message_id=message_id)
    except Exception as e:
        print(f"Error deleting message: {e}")
        #pass

def delete_button():
    markup = telebot.types.InlineKeyboardMarkup()
    button_del = telebot.types.InlineKeyboardButton("Close", callback_data='delete')
    markup.add(button_del)
    return markup
    
    
def create_refresh_button():
    markup = telebot.types.InlineKeyboardMarkup()
    refresh_button = telebot.types.InlineKeyboardButton("♻️Refresh🔄", callback_data='refresh')
    markup.add(refresh_button)
    return markup
    
def tombol_help() :
    markup = telebot.types.InlineKeyboardMarkup()
    help_button = telebot.types.InlineKeyboardButton("Minta Bantuan", callback_data='help')
    markup.add(help_button)
    return markup
    
def own_button():
    markup = telebot.types.InlineKeyboardMarkup()
    own_button= InlineKeyboardButton("🧑‍🚒Owner🧑‍🌾", url= "http://t.me/AlfiSyuhadak")
    markup.add()(own_button)
    return markup

def tombol_ganda():
    markup = telebot.types.InlineKeyboardMarkup()
    own_button=telebot.types.InlineKeyboardButton("🧑‍🌾Owner🧑‍🚒", url= "http://t.me/AlfiSyuhadak")
    help_button = telebot.types.InlineKeyboardButton("🤵Bantuan🤵", callback_data='help')
    refresh_button = telebot.types.InlineKeyboardButton("♻️Refresh🔄", callback_data='refresh')
    markup.add(help_button, refresh_button, own_button)
    return markup
    
    
def tombol_del() :
    markup = telebot.types.InlineKeyboardMarkup()
    del_button = telebot.types.InlineKeyboardButton("Tutup", callback_data='hapus')
    markup.add(help_button)
    return markup