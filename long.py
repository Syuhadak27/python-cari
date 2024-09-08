



def send_long_message_html(chat_id, message_text):
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
            
            
def send_long_message(chat_id, message_text):
        max_length = 4096
        for i in range(0, len(message_text), max_length):
            bot.send_message(chat_id, message_text[i:i+max_length])
