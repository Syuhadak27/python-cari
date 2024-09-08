import re
from Button import create_refresh_button, tombol_ganda, tombol_help
from pesan import KURANG_KATA, TIDAK_ADA, RESPON_TEXT
from delete import schedule_deletion
from delete import schedule_deletion
from cache import get_google_sheet_data

def handle_list(bot, message, LIST_ID, RANGE_LIST):
    query = message.text.split(' ', 1)[1] if len(message.text.split(' ', 1)) > 1 else ''
    
    if not query:
        msg = bot.reply_to(message, KURANG_KATA)
        schedule_deletion(bot, message.chat.id, msg.message_id, 1)
        schedule_deletion(bot, message.chat.id, message.message_id, 1)
        return
    
    query_parts = query.split()
    list_data = get_google_sheet_data(LIST_ID, RANGE_LIST)

    filtered_data = [row for row in list_data if all(re.search(re.escape(part), ' '.join(row), re.IGNORECASE) for part in query_parts)]

    response = f"{RESPON_TEXT} Kata Kunci : {query}\n\n"
    if filtered_data:
        for row in filtered_data:
            response += "•• `" + ' • '.join(row) + "`\n"
        schedule_deletion(bot, message.chat.id, message.message_id, 2)
    else:
        response = TIDAK_ADA
        msg = bot.send_message(message.chat.id, response, reply_markup=tombol_ganda(), parse_mode="Markdown")
        schedule_deletion(bot, message.chat.id, msg.message_id, 7)
        schedule_deletion(bot, message.chat.id, message.message_id, 2)
        return

    def send_long_message(chat_id, message_text):
        max_length = 4096
        while message_text:
            part = message_text[:max_length]
            if len(part) == max_length:
                last_index = part.rfind("`\n") + len("`\n")
                if last_index > 0:
                    part = message_text[:last_index]
                else:
                    part = message_text[:max_length]
            bot.send_message(chat_id, part, parse_mode="Markdown")
            message_text = message_text[len(part):]

    send_long_message(message.chat.id, response)