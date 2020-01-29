
BUTTON_INFO = 'ℹ️ INFO'
BUTTON_START_CONVERSION = '🔄 CONVERT'
BUTTON_BACK = '🔙 BACK'

MSG_INTRO = (
    "😎 Hi, I'm here to help you converting a csv file into tbx.\n\n"
    "Click on 🔄 CONVERT to start!"
)

MSG_SEND_CSV = (
    "📁 Send me a *csv file* with 9 fields (';' colon separated):\n" 
    "1. term(s)\n"
    "2. pos (e.g., N)\n"
    "3. internal pos (for mwe, e.g., NPN)\n"
    "4. morphology (4 characters, e.g., ms+-) - OPTIONAL\n"
    "5. variants (comma separated)\n"
    "6. synonyms (comma separated)\n"
    "7. definition - OPTIONAL\n"
    "8. hypernyms (comma separated)\n"
    "9. onthology class\n"
)

MSG_WRONG_EXTENSION = 'File extension not valid: it should end with ".csv"'

MSG_WRONG_INPUT = 'Wrong input'

MSG_ASK_LANGUAGE = 'Please insert *langauge* (e.g., en for English)'
MSG_ASK_SUBJECT = 'Please insert *subject* (e.g., Archeology)'
MSG_ASK_ID_PREFIX = 'Please insert the *id prefix* (e.g., RA)'
MSG_ASK_URI_TARGET = 'Please insert the *URI target* (e.g., http://www.cidoc-crm.org/cidoc-crm)'
MSG_ASK_URI_NAME = 'Please insert the *URI name* (e.g., CIDOC CRM)'

MSG_SEND_FILE_NO_TEXT = 'Please send me a *file* not a text in the chat.'

def wrong_input(text):
    reply = "Invalid input: {}"
    return reply.format(text)            
        
