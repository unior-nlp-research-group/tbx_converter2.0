
BUTTON_INFO = 'ℹ️ INFO'
BUTTON_START_CONVERSION = '🔄 CONVERT'
BUTTON_BACK = '🔙 BACK'
BUTTON_YES = '✅ YES'
BUTTON_NO = '❌ NO'



MSG_INTRO = (
    "😎 Hi, I'm here to help you converting a CSV file into TBX\n\n"
    "Click on 🔄 CONVERT to start!"
)

MSG_SEND_CSV_MULTI = (
    """📁 Send me {} *csv file* with 9 fields (';' semicolon separated)\n:""" 
    "1. term(s)\n"
    "2. pos (e.g., N)\n"
    "3. internal pos (for mwe, e.g., NPN) - OPTIONAL\n"
    "4. grammatical info (4 characters, e.g., ms+-) - OPTIONAL\n"
    "5. variants (comma separated) - OPTIONAL\n"
    "6. synonyms (comma separated) - OPTIONAL\n"
    "7. definition - OPTIONAL\n"
    "8. hypernyms (comma separated) - OPTIONAL\n"
    "9. ontology class - OPTIONAL\n\n"
    """*Important*: optional fields can be left empty but make sure there are 8
    semicolons per line.\n"""
    """*Important*: the order of these files has to follow the order of the
    input languages. """
    """*Important*: because they are used as separator, no semicolon might be
    used in the descriptions."""
)

MSG_SEND_CSV = (
    "📁 Send me a *csv file* with 9 fields (';' semicolon separated):\n" 
    "1. term(s)\n"
    "2. pos (e.g., N)\n"
    "3. internal pos (for mwe, e.g., NPN) - OPTIONAL\n"
    "4. grammatical info (4 characters, e.g., ms+-) - OPTIONAL\n"
    "5. variants (comma separated) - OPTIONAL\n"
    "6. synonyms (comma separated) - OPTIONAL\n"
    "7. definition - OPTIONAL\n"
    "8. hypernyms (comma separated) - OPTIONAL\n"
    "9. ontology class - OPTIONAL\n\n"
    "*Important*: optional fields can be left empty but make sure there are 8 semicolons per line."
)

MSG_WRONG_EXTENSION = 'File extension not valid: it should end with ".csv"'

MSG_WRONG_INPUT = 'Wrong input'


MSG_ASK_MULTIPLE_FILES = """You've sent {} files, you have to send {} more \
files."""
MSG_ASK_IF_MULTILINGUAL = "Are you working on more than one language?"
MSG_ASK_LANGUAGE_MULTI = """Please insert the *languages* separated by a comma
(e.g. it, en for Italian and English). """
MSG_ASK_LANGUAGE_MONO = 'Please insert *language* (e.g., en for English)'
MSG_ASK_SUBJECT = 'Please insert *subject* (e.g., Archaeology)'
MSG_ASK_ID_PREFIX = 'Please insert the *id prefix* (e.g., {})'
MSG_ASK_ONTOLOGY_YES_NO = 'Do you want to insert an ontology reference?'
MSG_ASK_ONTOLOGY_LINK = 'Please insert the *ontology link* (e.g., http://www.cidoc-crm.org/cidoc-crm)'
MSG_ASK_ONTOLOGY_NAME = 'Please insert the *ontology name* (e.g., CIDOC CRM)'
MSG_WARNING_SAME_ID= 'You have already entered this file'
MSG_SEND_FILE_NO_TEXT = 'Please send me a *file* not a text in the chat.'
MSG_FILE_READY = 'Your TBX file is ready.'

MSG_WRONG_ISO_CODE = """You entered a wrong ISO Code, please check your language
code at http://www.lingoes.net/en/translator/langcode.htm"""


def wrong_input(text):
    reply = "Invalid input: {}"
    return reply.format(text)            
        
