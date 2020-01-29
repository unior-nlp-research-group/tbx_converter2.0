import telegram
import key
import logging
import traceback
import bot_ui as ux
import parameters
import bot_ndb_user
from bot_ndb_user import NDB_User
from bot_telegram import send_message, send_text_document, report_master
import csv2tbx
import utility
from ndb_utils import client_context

BOT = telegram.Bot(token=key.TELEGRAM_API_TOKEN)

DISABLED = False

# ================================
# RESTART
# ================================
def restart(user):
    redirect_to_state(user, state_INITIAL)


# ================================
# REDIRECT TO STATE
# ================================
def redirect_to_state(user, new_function, message_obj=None):
    new_state = new_function.__name__
    if user.state != new_state:
        logging.debug("In redirect_to_state. current_state:{0}, new_state: {1}".format(str(user.state), str(new_state)))
        user.set_state(new_state)
    repeat_state(user, message_obj)


# ================================
# REPEAT STATE
# ================================

def repeat_state(user, message_obj=None):
    state = user.state
    if state is None:
        restart(user)
        return
    method = possibles.get(state)
    if not method:
        msg = "⚠️ User {} sent to unknown method state: {}".format(user.chat_id, state)
        report_master(msg)
        restart(user)
    else:
        method(user, message_obj)

# ================================
# Initial State
# ================================

def state_INITIAL(user, message_obj=None, **kwargs):    
    if message_obj is None:
        kb = [[ux.BUTTON_START_CONVERSION]]
        send_message(user, ux.MSG_INTRO, kb)
    else: 
        text_input = message_obj.text
        if text_input:            
            kb = user.get_keyboard()
            if text_input in utility.flatten(kb):
                if text_input == ux.BUTTON_START_CONVERSION:
                    user.reset_tmp_variables()
                    redirect_to_state(user, state_CONVERT_ASK_LANG)
            else:
                send_message(user, ux.MSG_WRONG_INPUT, kb)
        else:
            send_message(user, ux.MSG_WRONG_INPUT)


def state_CONVERT_ASK_LANG(user, message_obj=None, **kwargs):    
    if message_obj is None:
        kb = [[ux.BUTTON_BACK]]
        send_message(user, ux.MSG_ASK_LANGUAGE, kb)
    else: 
        text_input = message_obj.text
        if text_input:            
            kb = user.get_keyboard()
            if text_input in utility.flatten(kb):
                if text_input == ux.BUTTON_BACK:
                    redirect_to_state(user, state_INITIAL)
            else:
                user.set_tmp_variable('LANG', text_input)
                redirect_to_state(user, state_CONVERT_ASK_SUBJECT)
        else:
            send_message(user, ux.MSG_WRONG_INPUT)

def state_CONVERT_ASK_SUBJECT(user, message_obj=None, **kwargs):    
    if message_obj is None:
        kb = [[ux.BUTTON_BACK]]
        send_message(user, ux.MSG_ASK_SUBJECT, kb)
    else: 
        text_input = message_obj.text
        if text_input:            
            kb = user.get_keyboard()
            if text_input in utility.flatten(kb):
                if text_input == ux.BUTTON_BACK:
                    redirect_to_state(user, state_CONVERT_ASK_LANG)
            else:
                user.set_tmp_variable('SUBJECT', text_input)
                redirect_to_state(user, state_CONVERT_ASK_ID_PREFIX)
        else:
            send_message(user, ux.MSG_WRONG_INPUT)

def state_CONVERT_ASK_ID_PREFIX(user, message_obj=None, **kwargs):    
    if message_obj is None:
        kb = [[ux.BUTTON_BACK]]
        subject_upper_2_char = user.get_tmp_variable('SUBJECT').upper()[:2]
        send_message(user, ux.MSG_ASK_ID_PREFIX.format(subject_upper_2_char), kb)
    else: 
        text_input = message_obj.text
        if text_input:            
            kb = user.get_keyboard()
            if text_input in utility.flatten(kb):
                if text_input == ux.BUTTON_BACK:
                    redirect_to_state(user, state_CONVERT_ASK_SUBJECT)
            else:
                user.set_tmp_variable('ID_PREFIX', text_input)
                redirect_to_state(user, state_CONVERT_ASK_ONTOLOGY_YES_NO)
        else:
            send_message(user, ux.MSG_WRONG_INPUT)

def state_CONVERT_ASK_ONTOLOGY_YES_NO(user, message_obj=None, **kwargs):    
    if message_obj is None:
        kb = [[ux.BUTTON_YES, ux.BUTTON_NO],[ux.BUTTON_BACK]]
        send_message(user, ux.MSG_ASK_ONTOLOGY_YES_NO, kb)
    else: 
        text_input = message_obj.text
        if text_input:            
            kb = user.get_keyboard()
            if text_input in utility.flatten(kb):
                if text_input == ux.BUTTON_BACK:
                    redirect_to_state(user, state_CONVERT_ASK_ID_PREFIX)
                elif text_input == ux.BUTTON_YES:
                    redirect_to_state(user, state_CONVERT_ASK_ONTOLOGY_NAME)
                elif text_input == ux.BUTTON_NO:
                    user.set_tmp_variable('ONTOLOGY_NAME', None)
                    user.set_tmp_variable('ONTOLOGY_LINK', None)
                    redirect_to_state(user, state_CONVERT_ASK_DOC)                    
            else:
                send_message(user, ux.MSG_WRONG_INPUT)
        else:
            send_message(user, ux.MSG_WRONG_INPUT)

def state_CONVERT_ASK_ONTOLOGY_NAME(user, message_obj=None, **kwargs):    
    if message_obj is None:
        kb = [[ux.BUTTON_BACK]]
        send_message(user, ux.MSG_ASK_ONTOLOGY_NAME, kb)
    else: 
        text_input = message_obj.text
        if text_input:            
            kb = user.get_keyboard()
            if text_input in utility.flatten(kb):
                if text_input == ux.BUTTON_BACK:
                    redirect_to_state(user, state_CONVERT_ASK_ONTOLOGY_YES_NO)
            else:
                user.set_tmp_variable('ONTOLOGY_NAME', text_input)
                redirect_to_state(user, state_CONVERT_ASK_ONTOLOGY_LINK)
        else:
            send_message(user, ux.MSG_WRONG_INPUT)

def state_CONVERT_ASK_ONTOLOGY_LINK(user, message_obj=None, **kwargs):    
    if message_obj is None:
        kb = [[ux.BUTTON_BACK]]
        send_message(user, ux.MSG_ASK_ONTOLOGY_LINK, kb)
    else: 
        text_input = message_obj.text
        if text_input:            
            kb = user.get_keyboard()
            if text_input in utility.flatten(kb):
                if text_input == ux.BUTTON_BACK:
                    redirect_to_state(user, state_CONVERT_ASK_ONTOLOGY_NAME)
            else:
                user.set_tmp_variable('ONTOLOGY_LINK', text_input)
                redirect_to_state(user, state_CONVERT_ASK_DOC)
        else:
            send_message(user, ux.MSG_WRONG_INPUT)

def state_CONVERT_ASK_DOC(user, message_obj=None, **kwargs):    
    if message_obj is None:
        kb = [[ux.BUTTON_BACK]]
        send_message(user, ux.MSG_SEND_CSV, kb)
    else: 
        text_input = message_obj.text
        if text_input:            
            kb = user.get_keyboard()
            if text_input in utility.flatten(kb):
                if text_input == ux.BUTTON_BACK:
                    ontology_enabled = user.get_tmp_variable('ONTOLOGY_NAME') is not None
                    if ontology_enabled:
                        redirect_to_state(user, state_CONVERT_ASK_ONTOLOGY_LINK)
                    else:
                        redirect_to_state(user, state_CONVERT_ASK_ONTOLOGY_YES_NO)
            else:
                send_message(user, ux.MSG_SEND_FILE_NO_TEXT)
        elif message_obj.document:
            deal_with_document_request(user, message_obj.document)                
        else:
            send_message(user, ux.MSG_SEND_FILE_NO_TEXT)

def exception_reporter(func, *args, **kwargs):    
    def dec(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception:
            report_string = '❗️ Exception {}'.format(traceback.format_exc()) #.splitlines()
            logging.error(report_string)          
            try:  
                report_master(report_string)
            except Exception:
                report_string = '❗️ Exception {}'.format(traceback.format_exc())
                logging.error(report_string)          
    return dec

def run_new_thread_and_report_exception(func, *args, **kwargs):
    import threading   

    @exception_reporter
    def report_exception_in_thread(func, *args, **kwargs):
        func(*args,  **kwargs)

    args= list(args)
    args.insert(0, func)
    threading.Thread(target=report_exception_in_thread, args=args, kwargs=kwargs).start()
    

def set_webhook():
    s = BOT.setWebhook(key.WEBHOOK_TELEGRAM_BASE, allowed_updates=['message'])
    if s:
        print("webhook setup ok: {}".format(key.WEBHOOK_TELEGRAM_BASE))
    else:
        print("webhook setup failed")

def delete_webhook():
    BOT.deleteWebhook()

def get_webhook_info():
    print(BOT.get_webhook_info())

'''
python-telegram-bot documentation
https://python-telegram-bot.readthedocs.io/en/stable/
'''

@exception_reporter
@client_context
def deal_with_request(request_json):
    # retrieve the message in JSON and then transform it to Telegram object
    update_obj = telegram.Update.de_json(request_json, BOT)
    message_obj = update_obj.message    
    user_obj = message_obj.from_user
    chat_id = user_obj.id    
    username = user_obj.username
    last_name = user_obj.last_name if user_obj.last_name else ''
    name = (user_obj.first_name + ' ' + last_name).strip()

    user = bot_ndb_user.get_person_by_id_and_application(user_obj.id, 'telegram')

    if user == None:
        user = bot_ndb_user.add_person(chat_id, name, last_name, username, 'telegram')
        report_master('New user: {}'.format(user.get_first_last_username()))
    else:
        _, was_disabled = user.update_info(name, last_name, username)
        if was_disabled:
            msg = "Bot riattivato!"
            send_message(user, msg)
    
    if message_obj.text:
        if deal_with_commands(user, message_obj.text):
            return

    repeat_state(user, message_obj=message_obj)


def deal_with_commands(user, text):
    if text in ['/start', '/help', ux.BUTTON_INFO]:
        restart(user)
        return True
    if text == '/exception':
        1/0
        return True
    if text.startswith('/'):
        send_message(user, ux.wrong_input(text))    
        return True
    return False

def get_url_from_file_id(file_id):    
    import requests
    logging.debug("TELEGRAM: Requested file_id: {}".format(file_id))
    r = requests.post(key.TELEGRAM_API_URL + 'getFile', data={'file_id': file_id})
    r_json = r.json()
    if 'result' not in r_json or 'file_path' not in r_json['result']:
        logging.warning('No result found when requesting file_id: {}'.format(file_id))
        return None
    file_url = r_json['result']['file_path']
    return file_url

def get_raw_content_from_file(file_id):
    import requests
    file_url_suffix = get_url_from_file_id(file_id)
    file_url = key.TELEGRAM_API_URL_FILE + file_url_suffix
    r = requests.get(file_url)
    return r.content

def get_content_from_file(file_id):
    import requests
    file_url_suffix = get_url_from_file_id(file_id)
    file_url = key.TELEGRAM_API_URL_FILE + file_url_suffix
    r = requests.get(file_url)
    return r.content

def deal_with_photo_request(user, photo_list):
    reply_text = 'Photo input'
    send_message(user, reply_text)    

def deal_with_document_request(user, document_obj):          
    if DISABLED:
        reply_text = "Temporary disabled"
        send_message(user, reply_text, markdown=False)    
        return
    file_id = document_obj.file_id
    file_name = document_obj.file_name    
    mime_type = document_obj.mime_type
    file_size = document_obj.file_size #bytes    
    logging.debug('Receiving document: {}'.format(file_name))
    logging.debug("File size: {}".format(file_size))
    if file_size > 102400:
        reply_text = "File too big."
        send_message(user, reply_text)    
        return
    if file_name.endswith('.csv'):
        run_new_thread_and_report_exception(convert_csv_to_tbx, user, file_id, file_name)        
    else:
        send_message(user, ux.MSG_WRONG_EXTENSION)    
        return

@client_context
def convert_csv_to_tbx(user, file_id, file_name):
    import codecs
    from utility import check_file_encoding
    reply_text = "Conversion of `{}`, please wait ...".format(file_name)
    send_message(user, reply_text, markdown=False)    
    new_file_name = file_name.split('.')[0] + '.tbx'
    file_content = get_raw_content_from_file(file_id)             
    try:
        file_text = codecs.decode(file_content, 'utf-8')
    except UnicodeDecodeError:
        error_msg = "🤯 The file is not encoded as utf-8."
        send_message(user, error_msg, markdown=False)
    try:
        # import CsvFormatError, csv2tbx
        lines = file_text.splitlines()
        tbx_string = csv2tbx.csv2tbx(
            lines = lines,
            lang = user.get_tmp_variable('LANG'),
            subjectField = user.get_tmp_variable('SUBJECT'), 
            id_prefix = user.get_tmp_variable('ID_PREFIX'), 
            ontology_name = user.get_tmp_variable('ONTOLOGY_NAME'),
            ontology_link = user.get_tmp_variable('ONTOLOGY_LINK')
        )
        
    except csv2tbx.CsvFormatError as e:
        send_message(user, e.message, markdown=False)
    except Exception as e:
        error_msg = "🤯 Encountered problem to segment file {}. Please contact @kercos."
        send_message(user, error_msg, markdown=False)
    send_message(user, ux.MSG_FILE_READY, sleep=1)
    send_text_document(user, new_file_name, tbx_string)  
    restart(user)


possibles = globals().copy()
possibles.update(locals())