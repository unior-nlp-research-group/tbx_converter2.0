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
import csv2tbxmultil
import utility
from ndb_utils import client_context



iso_list = ['bh', 'ab', 'mr', 'ln', 'id', 'ps', 'tk', 'ce', 'ha', 'ba', 'os', 'el', 'gn', 'mt', 'ms', 'io', 'tn', 'ug', 'si', 'ff', 'ts', 'iu', 'fy', 'kk', 'be', 'nv', 'sr', 'or', 'rm', 'cv', 'de', 'cy', 'gu', 'pt', 'nd', 'lv', 'ie', 'cu', 'kl', 'et', 'tl', 'wa', 'xh', 'li', 'lb', 'kv', 'zh', 'sm', 'ho', 'qu', 'sn', 'fo', 'fj', 'sw', 'ti', 'kj', 'mi', 'ar', 'ko', 'za', 'aa', 'es', 'ta', 'oc', 'my', 'ja', 'lo', 'ne', 'kw', 'oj', 'eu', 'sa', 'wo', 'co', 'te', 'cs', 'ss', 'dv', 'lu', 'ay', 'bm', 'ga', 'nb', 'fi', 'hy', 'ru', 'af', 'sg', 'so', 'bo', 'nl', 'yo', 'mk', 'vi', 'uk', 'ng', 'da', 'ky', 'zu', 'ca', 'ht', 'ur', 'kr', 'bg', 'no', 'av', 'fr', 'bn', 'ig', 'tr', 'ki', 'om', 'uz', 'bs', 'nn', 'th', 'az', 'ks', 'gd', 'la', 'st', 'ia', 'cr', 'tg', 'am', 'ml', 'se', 'he', 'vo', 'to', 'eo', 'su', 'ee', 'kn', 'ku', 'hi', 'fa', 'ny', 'sl', 'br', 'kg', 'pi', 'lt', 'en', 'ak', 'rw', 'sc', 'gv', 'nr', 'sk', 'tw', 'gl', 'mg', 'sd', 'ik', 'as', 'hz', 've', 'pa', 'ch', 'dz', 'hr', 'jv', 'na', 'lg', 'rn', 'bi', 'is', 'ka', 'it', 'sq', 'ii', 'hu', 'ty', 'an', 'mh', 'pl', 'yi', 'ae', 'tt', 'sv', 'km', 'mn', 'ro']



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
                    redirect_to_state(user, state_ASK_IF_MULTILINGUAL)
            else:
                send_message(user, ux.MSG_WRONG_INPUT, kb)
        else:
           send_message(user, ux.MSG_WRONG_INPUT)


# ================================
# Following States
# ================================



def state_ASK_IF_MULTILINGUAL(user, message_obj=None, **kwargs):
    if message_obj is None:
        kb = [[ux.BUTTON_YES, ux.BUTTON_NO],[ux.BUTTON_BACK,]]
        send_message(user, ux.MSG_ASK_IF_MULTILINGUAL, kb)
    else: 
        text_input = message_obj.text
        if text_input:            
            kb = user.get_keyboard()
            if text_input in utility.flatten(kb):
                if text_input == ux.BUTTON_BACK:
                    redirect_to_state(user, state_INITIAL)
                elif text_input == ux.BUTTON_YES:
                    user.set_tmp_variable('IF_MULTI', True)
                    redirect_to_state(user, state_CONVERT_ASK_LANG_MULTI)
                elif text_input == ux.BUTTON_NO:
                    user.set_tmp_variable('IF_MULTI', False)
                    redirect_to_state(user, state_CONVERT_ASK_LANG_MULTI)
            else:
                send_message(user, ux.MSG_WRONG_INPUT)
        else:
            send_message(user, ux.MSG_WRONG_INPUT)

def state_CONVERT_ASK_LANG_MULTI(user, message_obj=None, **kwargs):
    if message_obj is None:
        kb = [[ux.BUTTON_BACK]]
        if user.get_tmp_variable('IF_MULTI') == True:
            send_message(user, ux.MSG_ASK_LANGUAGE_MULTI, kb)
        else:
            send_message(user, ux.MSG_ASK_LANGUAGE_MONO, kb)
    else: 
        text_input = message_obj.text
        if text_input:            
            kb = user.get_keyboard()
            if text_input in utility.flatten(kb):
                if text_input == ux.BUTTON_BACK:
                    redirect_to_state(user, state_ASK_IF_MULTILINGUAL)
            else:
                input_list = text_input.replace(' ', '')
                input_list = [i.lower() for i in input_list.split(',')]
                check_list = all(elem in iso_list for elem in input_list)
                if check_list:
                    user.set_tmp_variable('LANG_LIST', input_list)
                    user.set_tmp_variable('COUNTER',
                    0)
                    redirect_to_state(user, state_CONVERT_ASK_SUBJECT)
                else:
                    send_message(user, ux.MSG_WRONG_ISO_CODE)
                    redirect_to_state(user, state_ASK_IF_MULTILINGUAL)
        else:
            send_message(user, ux.MSG_WRONG_INPUT)



def state_CONVERT_ASK_LANG_MONO(user, message_obj=None, **kwargs):    
    if message_obj is None:
        kb = [[ux.BUTTON_BACK]]
        send_message(user, ux.MSG_ASK_LANGUAGE_MONO, kb)
    else: 
        text_input = message_obj.text
        if text_input:            
            kb = user.get_keyboard()
            if text_input in utility.flatten(kb):
                if text_input == ux.BUTTON_BACK:
                    redirect_to_state(user, state_ASK_IF_MULTILINGUAL)
            else:
                input_list = text_input.replace(' ', '')
                input_list = [i.lower() for i in input_list.split(',')]
                check_list = all(elem in iso_list for elem in input_list)
                if check_list:
                    user.set_tmp_variable('LANG', text_input)
                    redirect_to_state(user, state_CONVERT_ASK_SUBJECT)
                else:
                    send_message(user, ux.MSG_WRONG_ISO_CODE)
                    redirect_to_state(user, state_ASK_IF_MULTILINGUAL)
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
                    if user.get_tmp_variable('IF_MULTI') == False:
                        redirect_to_state(user, state_CONVERT_ASK_LANG_MULTI)
                    else:
                        redirect_to_state(user, state_CONVERT_ASK_LANG_MULTI)
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
                    if user.get_tmp_variable('IF_MULTI') == True:
                        redirect_to_state(user, state_CONVERT_ASK_DOC_MULTI)
                    if user.get_tmp_variable('IF_MULTI') == False:
                        redirect_to_state(user, state_CONVERT_ASK_DOC_MULTI)                    
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
                if user.get_tmp_variable('IF_MULTI') == True:
                    redirect_to_state(user, state_CONVERT_ASK_DOC_MULTI)
                elif user.get_tmp_variable('IF_MULTI') == False:
                    redirect_to_state(user, state_CONVERT_ASK_DOC_MULTI)
        else:
            send_message(user, ux.MSG_WRONG_INPUT)

def state_CONVERT_ASK_DOC_MULTI(user, message_obj=None, **kwargs):    
    counter = user.get_tmp_variable('COUNTER')
    lang_list = user.get_tmp_variable('LANG_LIST')
    print(counter)
    if counter < len(lang_list):      
        print(counter)
        if message_obj is None:
            kb = [[ux.BUTTON_BACK]]
            msg = ux.MSG_SEND_CSV_MULTI.format(len(lang_list)-counter, \
            lang_list)
            send_message(user, msg, kb)
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
                id, file_name = deal_with_document_request_multi(user,
                message_obj.document)
                language = str(lang_list[counter])
                user.set_tmp_variable(str(language)+'_file_id', id)
                user.set_tmp_variable(str(language)+'_filename', file_name)
                user.set_tmp_variable('COUNTER', counter+1)
                redirect_to_state(user, state_CONVERT_ASK_DOC_MULTI)
            else:
                send_message(user, ux.MSG_SEND_FILE_NO_TEXT)
    else:
        run_new_thread_and_report_exception(convert_csv_to_tbx_multi, user,
        lang_list)


def state_CONVERT_ASK_DOC_MONO(user, message_obj=None, **kwargs):    
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
                send_message(user, report_string)
            except Exception:
                report_string = '❗️ Exception {}'.format(traceback.format_exc())
                logging.error(report_string)
                send_message(user, report_string)
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


def deal_with_document_request_multi(user, document_obj):
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
    #if file_size > 102400:
    #    reply_text = "File too big."
    #    send_message(user, reply_text)    
    #    return
    #if file_name.endswith('.csv'):
    return file_id, file_name
    #else:
    #    send_message(user, ux.MSG_WRONG_EXTENSION)
    #    return
    #    redirect_to_state(user, state_CONVERT_ASK_DOC_MULTI) 
    
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
    #if file_size > 102400:
    #    reply_text = "File too big."
    #    send_message(user, reply_text)    
    #    return
    if file_name.endswith('.csv'):
        run_new_thread_and_report_exception(convert_csv_to_tbx, user, file_id, file_name)        
    else:
        send_message(user, ux.MSG_WRONG_EXTENSION)    
        return

@client_context

def convert_csv_to_tbx_multi(user, lang_list):
    import codecs
    from utility import check_file_encoding
    file_ids = []
    filenames = []
    for language in lang_list:
        file_ids.append(user.get_tmp_variable(str(language)+'_file_id'))
        filenames.append(user.get_tmp_variable(str(language)+'_filename'))
    reply_text = "Conversion of", ' '.join(filenames), " please wait...."
    send_message(user, reply_text, markdown=False)
    new_file_name = 'output.tbx'
    file_contents = [get_raw_content_from_file(i) for i in file_ids]
    file_texts = []
    for content in file_contents:
        ind = file_contents.index(content)
        try:
            file_text = codecs.decode(content, 'utf-8')
            file_texts.append(file_text)
        except UnicodeDecodeError:
            error_msg = """The file {} is not encoded as
            utf-8.""".format(filenames[ind])
            send_message(user, error_msg, markdown=False)
    inputs = []
    counter_errors = 0
    error_file = {}
    for i in range(len(file_texts)):
        file = file_texts[i]
        single_input = []
        error_file[filenames[i]] = []
        for row in file.splitlines():
            single_row = [str(k) for k in row.split(';')]
            if len(single_row) != 9:
                counter_errors += 1
                ind_row = file.splitlines().index(row)
                error_file[filenames[i]].append(ind_row)
            else:
                single_input.append(single_row)
                continue
        inputs.append(single_input)
    if counter_errors == 0:    
        tbx_string = csv2tbxmultil.csv2tbx(
        inputs = inputs,
        languages = lang_list,
        subjectField = user.get_tmp_variable('SUBJECT'),
        id_prefix = user.get_tmp_variable('ID_PREFIX'),
        ontology_name = user.get_tmp_variable('ONTOLOGY_NAME'),
        ontology_link = user.get_tmp_variable('ONTOLOGY_LINK')
        )
        send_message(user, ux.MSG_FILE_READY, sleep=1)
        send_text_document(user, new_file_name, tbx_string)
        restart(user)
    else:
        msg = """An error was encountered in the following file(s): \n"""
        print(error_file)
        msg_list = ''
        for file in list(error_file.keys()):
            if len(error_file[file]) >= 1:
                frase= file +  ' row(s) num: ' + str(error_file[file])+ '\n'
                msg_list += frase
        send_message(user, msg, markdown= False)
        send_message(user, msg_list, markdown=False)
        user.set_tmp_variable('COUNTER', 0) 
        redirect_to_state(user, state_CONVERT_ASK_DOC_MULTI) 
    

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
        #lines = file_text.splitlines()
        tbx_string = csv2tbx.csv2tbx(
            lines = file_text,
            lang = user.get_tmp_variable('LANG'),
            subjectField = user.get_tmp_variable('SUBJECT'), 
            id_prefix = user.get_tmp_variable('ID_PREFIX'), 
            ontology_name = user.get_tmp_variable('ONTOLOGY_NAME'),
            ontology_link = user.get_tmp_variable('ONTOLOGY_LINK')
        )
    
        send_message(user, ux.MSG_FILE_READY, sleep=1)
        send_text_document(user, new_file_name, tbx_string)  
        restart(user)
    except csv2tbx.CsvFormatError as e:
        send_message(user, e.message, markdown=False)
    except Exception as e:
        error_msg = """🤯 Encountered problem to segment file {}. Please contact
        @kercos.""".format(e)
        send_message(user, error_msg, markdown=False)
        restart(user)

possibles = globals().copy()
possibles.update(locals())
