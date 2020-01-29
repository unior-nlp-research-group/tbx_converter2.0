import telegram
import telegram.error
from telegram.error import TelegramError, Unauthorized, BadRequest, TimedOut, ChatMigrated, NetworkError
# from main_exception import retry_on_network_error
import key
import logging
import traceback
import time
import bot_ndb_user
from bot_ndb_user import NDB_User
from ndb_utils import client_context

BOT = telegram.Bot(token=key.TELEGRAM_API_TOKEN)

'''
If kb==None keep last keyboard
'''
# @retry_on_network_error
def send_message(p, text, kb=None, markdown=True, remove_keyboard=False, \
    inline_keyboard=False, sleep=False, **kwargs):
    if kb or remove_keyboard:
        if inline_keyboard:
            reply_markup = {  
                'inline_keyboard': kb
            }
        elif remove_keyboard:
            p.set_keyboard(kb=[])            
            reply_markup = telegram.ReplyKeyboardRemove()
        else:
            p.set_keyboard(kb)
            reply_markup = telegram.ReplyKeyboardMarkup(kb, resize_keyboard=True)
        BOT.send_message(
            chat_id = p.chat_id,
            text = text,
            parse_mode = telegram.ParseMode.MARKDOWN if markdown else None,
            reply_markup = reply_markup,
            **kwargs
        )
    else:
        try:
            BOT.send_message(
                chat_id = p.chat_id,
                text = text,
                parse_mode = telegram.ParseMode.MARKDOWN if markdown else None,
                **kwargs
            )
        except Unauthorized:
            logging.debug('User has blocked Bot: {}'.format(p.chat_id))
            p.switch_notifications()
            return False
        except TelegramError as e:
            logging.debug('Exception in reaching user {}: {}'.format(p.chat_id, e))
            p.switch_notifications()
            return False
    if sleep:
        time.sleep(0.1)
    return True

def send_location(p, lat, lon):
    loc = telegram.Location(lon,lat)
    BOT.send_location(p.chat_id, location = loc)

def send_typing_action(p, sleep_time=None):    
    BOT.sendChatAction(
        chat_id = p.chat_id,
        action = telegram.ChatAction.TYPING
    )
    if sleep_time:
        time.sleep(sleep_time)


def send_media_url(p, url_attachment, kb=None, caption=None):
    attach_type = url_attachment.split('.')[-1].lower()            
    if attach_type in ['jpg','png','jpeg']:
        BOT.send_photo(p.chat_id, photo=url_attachment, caption=caption)
    elif attach_type in ['mp3']:
        BOT.send_audio(p.chat_id, audio=url_attachment, caption=caption)
    elif attach_type in ['ogg']:
        BOT.send_voice(p.chat_id, voice=url_attachment, caption=caption)       
    elif attach_type in ['gif']:        
        BOT.send_animation(p.chat_id, animation=url_attachment, caption=caption)
    elif attach_type in ['mp4']:
        BOT.send_audio(p.chat_id, audio=url_attachment, caption=caption)
    else:            
        error_msg = "Found attach_type: {}".format(attach_type)
        logging.error(error_msg)
        raise ValueError('Wrong attach type: {}'.format(error_msg))

def send_text_document(p, file_name, file_content):
    import requests
    files = [('document', (file_name, file_content, 'text/plain'))]
    data = {'chat_id': p.chat_id}
    resp = requests.post(key.TELEGRAM_API_URL + 'sendDocument', data=data, files=files)
    logging.debug("Sent documnet. Response status code: {}".format(resp.status_code))

def get_photo_url_from_telegram(file_id):
    import requests
    r = requests.post(key.TELEGRAM_API_URL + 'getFile', data={'file_id': file_id})
    r_json = r.json()
    r_result = r_json['result']
    file_path = r_result['file_path']
    url = key.TELEGRAM_API_URL_FILE + file_path
    return url

bot_telegram_MASTER = None

def report_master(message):
    global bot_telegram_MASTER
    if bot_telegram_MASTER is None:
        bot_telegram_MASTER = bot_ndb_user.get_person_by_id(key.TELEGRAM_BOT_MASTER_ID)
    max_length = 2000
    if len(message)>max_length:
        chunks = (message[0+i:max_length+i] for i in range(0, len(message), max_length))
        for m in chunks:
            send_message(bot_telegram_MASTER, m, markdown=False)    
    else:
        send_message(bot_telegram_MASTER, message, markdown=False)
