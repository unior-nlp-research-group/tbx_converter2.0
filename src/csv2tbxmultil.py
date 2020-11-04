import pandas as pd
import lxml
from lxml import etree



class CsvFormatError(Exception):
    def __init__(self, message):
        self.message = message

POS_MAPPING_OTHER = 'other'

iso_codes = ['aw', 'af', 'ao', 'ai', 'ax', 'al', 'ad', 'ae', 'ar', 'am', 'as', 'aq', 'tf', 'ag', 'au', 'at', 'az', 'bi', 'be', 'bj', 'bq', 'bf', 'bd', 'bg', 'bh', 'bs', 'ba', 'bl', 'by', 'bz', 'bm', 'bo', 'br', 'bb', 'bn', 'bt', 'bv', 'bw', 'cf', 'ca', 'cc', 'ch', 'cl', 'cn', 'ci', 'cm', 'cd', 'cg', 'ck', 'co', 'km', 'cv', 'cr', 'cu', 'cw', 'cx', 'ky', 'cy', 'cz', 'de', 'dj', 'dm', 'dk', 'do', 'dz', 'ec', 'eg', 'er', 'eh', 'es', 'ee', 'et', 'fi', 'fj', 'fk', 'fr', 'fo', 'fm', 'ga', 'gb', 'ge', 'gg', 'gh', 'gi', 'gn', 'gp', 'gm', 'gw', 'gq', 'gr', 'gd', 'gl', 'gt', 'gf', 'gu', 'gy', 'hk', 'hm', 'hn', 'hr', 'ht', 'hu', 'id', 'im', 'in', 'io', 'ie', 'ir', 'iq', 'is', 'il', 'it', 'jm', 'je', 'jo', 'jp', 'kz', 'ke', 'kg', 'kh', 'ki', 'kn', 'kr', 'kw', 'la', 'lb', 'lr', 'ly', 'lc', 'li', 'lk', 'ls', 'lt', 'lu', 'lv', 'mo', 'mf', 'ma', 'mc', 'md', 'mg', 'mv', 'mx', 'mh', 'mk', 'ml', 'mt', 'mm', 'me', 'mn', 'mp', 'mz', 'mr', 'ms', 'mq', 'mu', 'mw', 'my', 'yt', 'na', 'nc', 'ne', 'nf', 'ng', 'ni', 'nu', 'nl', 'no', 'np', 'nr', 'nz', 'om', 'pk', 'pa', 'pn', 'pe', 'ph', 'pw', 'pg', 'pl', 'pr', 'kp', 'pt', 'py', 'ps', 'pf', 'qa', 're', 'ro', 'ru', 'rw', 'sa', 'sd', 'sn', 'sg', 'gs', 'sh', 'sj', 'sb', 'sl', 'sv', 'sm', 'so', 'pm', 'rs', 'ss', 'st', 'sr', 'sk', 'si', 'se', 'sz', 'sx', 'sc', 'sy', 'tc', 'td', 'tg', 'th', 'tj', 'tk', 'tm', 'tl', 'to', 'tt', 'tn', 'tr', 'tv', 'tw', 'tz', 'ug', 'ua', 'um', 'uy', 'us', 'uz', 'va', 'vc', 've', 'vg', 'vi', 'vn', 'vu', 'wf', 'ws', 'ye', 'za', 'zm', 'zw']

POS_MAPPING = {
    'N': 'noun',
    'NP': 'noun',
    'NOUt': 'noun',
    'A': 'adjective',
    'ADJ': 'adjective',
    'V': 'verb',
    'VERB': 'verb',
}

inputs = []
langs = []

def csv2tbx(inputs, languages, subjectField, id_prefix, ontology_name=None,
ontology_link = None):
    
    languages_dict = {}
    for x in range(len(languages)):
        languages_dict["language_{0}".format(x)] = languages[x]

    dict_files = {}
    for x in range(len(inputs)):
        try:
            dict_files["csv_reader{0}".format(x)] = pd.DataFrame(inputs[x][1:],
            columns = inputs[x][0])
        except AssertionError as error:
                error_msg = """Error in input csv"""
                raise CsvFormatError(error_msg)

    keys = list(dict_files.keys())

    #determine which csv file has the most rows, it will be then used as the
    #'center'

    csv_files_shape = []

    for x in dict_files.keys():
        csv_files_shape.append(dict_files[x].shape)

    longest_csv_index = csv_files_shape.index(max(csv_files_shape))     

    list_filenames = [x for x in dict_files.keys()]
    longest_csv = list_filenames[longest_csv_index]
        

    parser = etree.XMLParser(remove_blank_text=True)
    root_xml =     """ \
        <martif type="TBX-Default" xml:lang="en"> 
        <martifHeader>
            <fileDesc> 
            <sourceDesc>
               <p>This is a TBX file generated via csv2tbx. Address any
    enquires to UniOr NLP Research Group at uniornlp@gmail.com </p>
            </sourceDesc> 
            </fileDesc>
            <encodingDesc>
            <p type="XCSURI">TBXXCS.xcs</p>
            </encodingDesc>
        </martifHeader>
        </martif> 
        """


    root = etree.XML(root_xml, parser)

    text_struct = etree.SubElement(root, "text")
    body_struct = etree.SubElement(text_struct, "body")

    
    max_num_rows = dict_files[longest_csv].shape[0]
    print(max_num_rows)
    
    for i in range(max_num_rows):
        
        id_str = "{}_{}".format(id_prefix, i+1)
        
        termEntry_struct = etree.SubElement(body_struct, "termEntry", \
        id=id_str)
        #descriptGrp_struct = etree.SubElement(termEntry_struct,
        #"descripGrp")

        if ontology_name:
            descriptGrp_struct = etree.SubElement(termEntry_struct, \
            "descripGrp")
            etree.SubElement(descriptGrp_struct, "descrip", \
            type="subjectField").text = subjectField
            etree.SubElement(descriptGrp_struct, "xref", type="URI", \
            target=ontology_link).text = '{} {}'.format(ontology_name, \
            'Ontology')
        else:
            etree.SubElement(termEntry_struct, "descrip", \
            type="subjectField").text = subjectField



        for filename in list_filenames:
            file_index = list_filenames.index(filename)
            
            try:
                row = dict_files[filename].iloc[i]        
                
                #todo aggiustare il messaggio di errore il nome del file
                #visualizzato sia effettivamente quello inserito dall'utente
                if len(row) != 9:
                    error_msg = """Error in input CSV: line {} in file {} has {} fields
                    instead of 9""".format(i, filename, len(row))
                    raise CsvFormatError(error_msg)


                if type(row[0]) == str:
                   
                    langSet_struct = etree.SubElement(termEntry_struct, "langSet")
                    attr = langSet_struct.attrib
                    attr['{http://www.w3.org/XML/1998/namespace}lang'] = \
                    languages[file_index]
                    
                    if type(row[6]) != float and len(row[6]) >= 1:
                        #descriptGrp_struct = etree.SubElement(langSet_struct,
                        #"descripGrp")
                        #langSet_struct_descr = etree.SubElement(descriptGrp_struct,
                        #"langSet")
                        #attr_lang_descr = langSet_struct_descr.attrib
                        #attr_lang_descr['{http://www.w3.org/XML/1998/namespace}lang'] = \
                        #languages[file_index]
                        
                        etree.SubElement(langSet_struct, "descrip",
                        type="definition").text = row[6]

                    
                    if type(row[2]) ==  str:
                        field_3_mw_pos_upper = row[2].upper()
                            
                    field_1_term = row[0]
                    field_2_pos_upper = row[1].upper()
           
                   
                    pos_full = POS_MAPPING.get(field_2_pos_upper,
                    POS_MAPPING_OTHER)

                    gender_full, number_full = None, None

                    if row[3] == str:
                        if len(row[3]) != 4:
                            error_msg = """Error in input CSV: line {} in
                            document {} is supposed to be 4 characters long
                            (e.g. 'ms+-')""".format(i, filename)
                            raise CsvFormatError(error_msg)
                        
                        if row[3][0] not in ['m','f']:
                            error_msg = """Error in input CSV: line {} in
                            document {} :
                                first character should be m (masculine) or f
                                (feminine)""".format(n,filename) 
                            raise CsvFormatError(error_msg)
                        if row[3][1] not in ['s','p']:
                            error_msg = """Error in input CSV: line {} in
                            document {}:
                                second character should be s (singular) or p
                                (plural)""".format(n, filename)
                            raise CsvFormatError(error_msg)
                        gender_full = 'masculine' if row[5][0]=='m' else 'feminine'
                        number_full = 'singular' if row[5][1]=='s' else 'plural'


                    use_ntig = ' ' in row[0] and row[2] 

                    ntig_tig_struct_tag = "ntig" if use_ntig else """tig"""
                    ntig_tig_struct = etree.SubElement(langSet_struct,
                    ntig_tig_struct_tag)

                    if use_ntig:
                        field_1_words = row[0].split() #lista di parole
                        pos_internal = [POS_MAPPING.get(x, POS_MAPPING_OTHER) \
                        for x in field_3_mw_pos_upper]
                        termGrp_struct = etree.SubElement(ntig_tig_struct,
                        "termGrp")
                        parent_node = termGrp_struct
                    else:
                        parent_node = ntig_tig_struct


                    etree.SubElement(parent_node, 'term').text = row[0]
                    etree.SubElement(parent_node, 'termNote', \
                    type="termType").text = "fullForm"

                    etree.SubElement(parent_node, 'termNote', \
                    type="partOfSpeech").text = pos_full

                    if gender_full and number_full:
                        etree.SubElement(parent_node, 'termNote', \
                        type="grammaticalGender").text = gender_full

                        etree.SubElement(parent_node, 'termNote', \
                        type="grammaticalNumber").text = number_full



                    if ontology_link and ontology_name and len(row[8]) >= 1:
                        ontology_link_term = '{}/{}'.format(ontology_link, \
                        row[8])
                        etree.SubElement(parent_node, "xref", type="URI",
                        target=ontology_link_term).text = """{} 
                        {}""".format(ontology_name, 'Class')



                    if use_ntig:
                        termCompList_struct = etree.SubElement(parent_node, \
                        "termCompList", type="lemma")
                        for o, w in enumerate(field_1_words):
                            termCompGrp_struct = \
                            etree.SubElement(termCompList_struct, \
                            "termCompGrp")

                            etree.SubElement(termCompGrp_struct,
                            "termComp").text = w

                            etree.SubElement(termCompGrp_struct, "termNote", \
                            type = "partOfSpeech").text = pos_internal[o]
                    if type(row[4]) == str and len(row[4]) >= 1:
                        for n, v in enumerate(row[4].split(',')):
                            v_num = str(n).zfill(2)
                            etree.SubElement(parent_node, "termNote", \
                            type="variant{}".format(v_num)).text = v
                    
                    if type(row[5]) == str and len(row[5]) >= 1:
                        for n, s in enumerate(row[5].split(',')):
                            s_num = str(n).zfill(2)
                            etree.SubElement(parent_node, "termNote", \
                            type="synonym{}".format(s_num)).text = s

                    if type(row[7]) == str and len(row[7]) >= 1:
                        for n, h in enumerate(row[7].split()):
                            h_num = str(n).zfill(2)
                            etree.SubElement(parent_node, "termNote", \
                            type="hypernyms{}".format(h_num)).text = h
                      
            except IndexError:
                pass
                
    tbx_string = etree.tostring(
        root,
        pretty_print=True,
        xml_declaration=True,
        doctype='<!DOCTYPE martif SYSTEM "TBXcoreStructV02.dtd">',
        encoding='UTF-8'
        )


    return tbx_string    



if __name__ == '__main__':
    
    tbx_string = csv2tbx(
        inputs = ['../data/glossario_it.csv',
        """../data/glossario_en.csv""",
        ],
        languages = ['it', 'en'],
        subjectField = "Archeology",
        id_prefix = 'RA',
        ontology_link = 'http://www.cidoc-crm.org/cidoc-crm',
        ontology_name = 'CIDOC CRM'
        )

    with open("../data/output.tbx", "wb") as f_out:
        f_out.write(tbx_string)










