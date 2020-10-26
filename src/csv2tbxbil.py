from lxml import etree
import csv
import pandas as pd

class CsvFormatError(Exception):
    def __init__(self, message):
        self.message = message

POS_MAPPING_OTHER = 'other'

POS_MAPPING = {
    'N': 'noun',
    'NP': 'noun',
    'NOUN': 'noun',
    'A': 'adjective',
    'ADJ': 'adjective',
    'V': 'verb',
    'VERB': 'verb',
}

def csv2tbx(input_l1, input_l2, lang1, lang2, subjectField, id_prefix, ontology_name=None, ontology_link=None):

    parser = etree.XMLParser(remove_blank_text=True)
    root_xml = \
        '''\
        <martif type="TBX-Default" xml:lang="en">
        <martifHeader>
            <fileDesc>
            <sourceDesc>
                <p>This is a TBX file generated via .... Address any enquiries to ....</p>
            </sourceDesc>
            </fileDesc>
            <encodingDesc>
            <p type="XCSURI">TBXXCS.xcs</p>
            </encodingDesc>
        </martifHeader>
        </martif>
        '''
        # -> to verify xcs

    root = etree.XML(root_xml, parser)

    text_struct = etree.SubElement(root, "text")
    body_struct = etree.SubElement(text_struct, "body")

    csv_reader_l1 = pd.read_csv(input_l1)
    csv_reader_l2 = pd.read_csv(input_l2)
###per debug, eliminare in seguito!!!!
    csv_reader_l1 = csv_reader_l1.drop(columns=csv_reader_l1.columns[0])
    csv_reader_l2 = csv_reader_l2.drop(columns=csv_reader_l2.columns[0])
  

    for n_l1,row_l1 in csv_reader_l1.iterrows():
        if len(row_l1) != 9:
            error_msg = "Error in input CSV: line {} has {} fields instead of \
            9".format(n_l1, len(row_l1))
            raise CsvFormatError(error_msg)
       # row = [x.strip() for x in row if type(x) == str]
        field_1_term_l1 = row_l1[0]
        field_2_pos_upper_l1= row_l1[1].upper()
        if type(row_l1[2]) != float :
            field_3_mw_pos_upper_l1 = row_l1[2].upper()
        else:
            field_3_mw_pos_upper_l1 = ''
        if type(row_l1[3]) != float :
            field_4_flex_lower_l1 = row_l1[3].lower()
        else:
            field_4_flex_lower_l1 = ''
        if type(row_l1[4]) != float :
            field_5_variants_l1 = [x.strip() for x in row_l1[4].split(',') if type(x) ==
        str]
        else:
            field_5_variants_l1= ''
        if type(row_l1[5]) != float:
            field_6_synonyms_l1 = [x.strip() for x in row_l1[5].split(',') if type(x) ==
        str]
        else:
            field_6_synonyms_l1= ''
        if type(row_l1[6]) != float:
            field_7_desc_l1 = row_l1[6]
        else:
            field_7_desc_l1 = ''
        if type(row_l1[7]) != float:
            field_8_hyper_l1 = [x.strip() for x in row_l1[7].split(',') if type(x) == str]
        else:
            field_8_hyper_l1 = ''
        if type(row_l1[8]) != float:
            field_9_class_l1= row_l1[8]
        else:
            field_9_class_l1 = ''
        use_ntig = field_3_mw_pos_upper_l1


        
########################################l2 time

        row_l2 = csv_reader_l2.iloc[n_l1]

        if len(row_l2) != 9:
            error_msg = "Error in input CSV: line {} has {} fields instead of 9".format(n, len(row_l2))
            raise CsvFormatError(error_msg)
       # row = [x.strip() for x in row_l2 if type(x) == str]
        field_1_term_l2 = row_l2[0]
        if type(row_l2[1]) == str:
            field_2_pos_upper_l2= row_l2[1].upper()
        else:
            field_2_pos_upper_l2 = ''
        if type(row_l2[2]) == str :
            field_3_mw_pos_upper_l2 = row_l2[2].upper()
        else:
            field_3_mw_pos_upper_l2 = ''
        if type(row_l2[3]) == str :
            field_4_flex_lower_l2 = row_l2[3].lower()
        else:
            field_4_flex_lower_l2 = ''
        if type(row_l2[4]) == str :
            field_5_variants_l2 = [x.strip() for x in row_l2[4].split(',') if type(x) ==
        str]
        else:
            field_5_variants_l2= ''
        if type(row_l2[5]) == str:
            field_6_synonyms_l2 = [x.strip() for x in row_l2[5].split(',') if type(x) ==
        str]
        else:
            field_6_synonyms_l2= ''
        if type(row_l2[6]) ==  str:
            field_7_desc_l2 = row_l2[6]
        else:
            field_7_desc_l2 = ''
        if type(row_l2[7]) == str:
            field_8_hyper_l2 = [x.strip() for x in row_l2[7].split(',') if type(x) == str]
        else:
            field_8_hyper_l2 = ''
        if type(row_l2[8]) == str:
            field_9_class_l2= row_l2[8]
        else:
            field_9_class_l2 = ''
        use_ntig = field_3_mw_pos_upper_l2




##############################################

        #pos mapping

        pos_full_l1 = POS_MAPPING.get(field_2_pos_upper_l1, POS_MAPPING_OTHER)
        pos_full_l2 = POS_MAPPING.get(field_2_pos_upper_l2,
        POS_MAPPING_OTHER)


        gender_full_l1, number_full_l1 = None, None
        gender_full_l2, number_full_l2 = None, None


        if field_4_flex_lower_l1:
            if len(field_4_flex_lower_l1)!=4:
                error_msg = "Error in input CSV: line {} has error in field 4 ({}): \
                    inflection should be 4 characters long (e.g., ms+-)".format(n, field_4_flex_lower_l1)
                raise CsvFormatError(error_msg)
            if field_4_flex_lower_l1[0] not in ['m','f']:
                error_msg = """Error in input CSV: line {} has error in field 4 ({}): \
                    first character should be m (masculine) or f (feminine)""".format(n, field_4_flex_lower_l1)
                raise CsvFormatError(error_msg)
            if field_4_flex_lower_l1[1] not in ['s','p']:
                error_msg = """Error in input CSV: line {} has error in field 4 ({}): \
                    second character should be s (singular) or p (plural)""".format(n, field_4_flex_lower_l1)
                raise CsvFormatError(error_msg)
            gender_full_l1= 'masculine' if field_4_flex_lower_l1[0]=='m' else 'feminine'
            number_full_l1 = 'singular' if field_4_flex_lower_l1[1]=='s' else 'plural'

        
        if field_4_flex_lower_l2:
            if len(field_4_flex_lower_l2)!=4:
                error_msg = """Error in input CSV: line {} has error in field 4 ({}): \
                    inflection should be 4 characters long  
                    (e.g., ms+-)""".format(n, field_4_flex_lower_l2) 
                raise CsvFormatError(error_msg)
            if field_4_flex_lower_l2[0] not in ['m','f']:
                error_msg = """Error in input CSV: line {} has error in field 4 ({}): \
                    first character should be m (masculine) or f
                    (feminine)""".format(n, field_4_flex_lower_l2)
                raise CsvFormatError(error_msg)
            if field_4_flex_lower_l2[1] not in ['s','p']:
                error_msg = """Error in input CSV: line {} has error in field 4 ({}): \
                    second character should be s (singular) or p
                    (plural)""".format(n, field_4_flex_lower_l2)
                raise CsvFormatError(error_msg)
            gender_full_l2= 'masculine' if field_4_flex_lower_l2[0]=='m' else 'feminine'
            number_full_l2 = 'singular' if field_4_flex_lower_l2[1]=='s' else 'plural'


######################################

        #multiword

        # term is multi word if first field has spaces and third field (interal structure) is present
        use_ntig_l1 = ' ' in field_1_term_l1 #and field_3_mw_pos_upper_l1 
        if type(field_1_term_l2) == str:
            use_ntig_l2 = ' ' in field_1_term_l2 #and field_3_mw_pos_upper_l2
        else:
            use_ntig_l2 = False
##########################################

        #id and subject

        id_str = "{}_{}".format(id_prefix, n_l1+1)
        # <termEntry id="RA_286">
        termEntry_struct = etree.SubElement(body_struct, "termEntry", id=id_str)
        descripGrp_struct = etree.SubElement(termEntry_struct, "descripGrp")
        # <descrip type="subjectField">Archaeology</descrip> 
        etree.SubElement(descripGrp_struct, "descrip", type="subjectField").text = subjectField
        

        

        if field_7_desc_l1:
            # <descrip type="definition">Definition Text</descrip>
            etree.SubElement(descripGrp_struct, "descrip", type="definition").text = field_7_desc_l1
        
        if field_7_desc_l2:
            etree.SubElement(descripGrp_struct, "descript",
            type="definition").text = field_7_desc_l2

        # <xref type="URI" target= "http://www.cidoc-crm.org/cidoc-crm">CIDOC CRM Ontology</xref>
        if ontology_name:
            etree.SubElement(descripGrp_struct, "xref", type="URI", target=ontology_link).text = '{} {}'.format(ontology_name, 'Ontology')                
        



####################

        #language sets

        # <langSet xml:lang="it">
        langSet_struct_l1 = etree.SubElement(termEntry_struct, "langSet") #attrib={'xml:lang':lang}
        attr_l1 = langSet_struct_l1.attrib
        attr_l1['{http://www.w3.org/XML/1998/namespace}lang'] = lang1

        
        langSet_struct_l2 = etree.SubElement(termEntry_struct, "langSet")
        attr_l2 = langSet_struct_l2.attrib
        attr_l2['{http://www.w3.org/XML/1998/namespace}lang'] = lang2
        
###########################
        
        ntig_tig_struct_tag_l1 = "ntig" if use_ntig_l1 else "tig"
        ntig_tig_struct_l1 = etree.SubElement(langSet_struct_l1,
        ntig_tig_struct_tag_l1)

       
        if use_ntig:
            field_1_words_l1 = row_l1[0].split() # lista di parole      
            pos_internal_l1 = [POS_MAPPING.get(x, POS_MAPPING_OTHER) for x in field_3_mw_pos_upper_l1]          

            termGrp_struct_l1 = etree.SubElement(ntig_tig_struct_l1, "termGrp")
            parent_node_l1 = termGrp_struct_l1
        else:
            parent_node_l1 = ntig_tig_struct_l1


        ntig_tig_struct_tag_l2 = "ntig" if use_ntig_l2 else "tig"
        ntig_tig_struct_l2 = etree.SubElement(langSet_struct_l2,
        ntig_tig_struct_tag_l2)

       
        if use_ntig_l2:
            field_1_words_l2 = row_l2[0].split() # lista di parole      
            pos_internal_l2 = [POS_MAPPING.get(x, POS_MAPPING_OTHER) for x in
            field_3_mw_pos_upper_l2]          

            termGrp_struct_l2 = etree.SubElement(ntig_tig_struct_l2, "termGrp")
            parent_node_l2 = termGrp_struct_l2
        else:
            parent_node_l2 = ntig_tig_struct_l2

#####################################


        # <term>dinos con anse ad anello</term>
        etree.SubElement(parent_node_l1, 'term').text = row_l1[0]
        if type(row_l2[0]) == str:
            etree.SubElement(parent_node_l2, 'term').text = row_l2[0]
        else:
            pass
        # <termNote type="termType">fullForm</termNote>
        etree.SubElement(parent_node_l1, 'termNote', type="termType").text = 'fullForm'
        etree.SubElement(parent_node_l2, 'termNote', type="termType").text = \
        'fullForm'

        # <termNote type="partOfSpeech">noun</termNote>
        etree.SubElement(parent_node_l1, 'termNote', \
        type="partOfSpeech").text=pos_full_l1 

        etree.SubElement(parent_node_l2, 'termNote', \
        type="partOfSpeech").text = pos_full_l2

        
#########################################

        if gender_full_l1 and number_full_l1:
            # <termNote type="grammaticalGender">masculine</termNote>
            etree.SubElement(parent_node_l1, 'termNote', type="grammaticalGender").text = gender_full_l1
            # <termNote type="grammaticalNumber">singular</termNote>
            etree.SubElement(parent_node_l1, 'termNote', type="grammaticalNumber").text = number_full_l1
        # <xref type="URI" target="http://www.cidoc-crm.org/cidoc-crm/E22">CIDOC CRM Class</xref>
        
        if gender_full_l2 and number_full_l2:
            # <termNote type="grammaticalGender">masculine</termNote>
            etree.SubElement(parent_node_l2, 'termNote',
            type="grammaticalGender").text = gender_full_l2
            # <termNote type="grammaticalNumber">singular</termNote>
            etree.SubElement(parent_node_l2, 'termNote',
            type="grammaticalNumber").text = number_full_l2
        # <xref type="URI" target="http://www.cidoc-crm.org/cidoc-crm/E22">CIDOC CRM Class</xref>
        

        if ontology_link and ontology_name:
            ontology_link_term = '{}/{}'.format(ontology_link, field_9_class_l1)
            etree.SubElement(parent_node_l1, "xref", type="URI", target=ontology_link_term).text = '{} {}'.format(ontology_name, 'Class')                




        if use_ntig_l1:
            # <termCompList type="lemma">
            termCompList_struct = etree.SubElement(parent_node_l1, "termCompList", type="lemma")
            for i, word in enumerate(field_1_words_l1):
                termCompGrp_struct = etree.SubElement(termCompList_struct_l1, "termCompGrp")
                # <termComp>dinos</termComp>
                etree.SubElement(termCompGrp_struct_l1, "termComp").text = word
                # <termNote type="partOfSpeech">noun</termNote>
                etree.SubElement(termCompGrp_struct_l1, "termNote",
                type="partOfSpeech").text = pos_internal_l1[i]

        
        if use_ntig_l2:
            # <termCompList type="lemma">
            termCompList_struct = etree.SubElement(parent_node_l2, "termCompList", type="lemma")
            for i, word in enumerate(field_1_words_l2):
                termCompGrp_struct = etree.SubElement(termCompList_struct_l2, "termCompGrp")
                # <termComp>dinos</termComp>
                etree.SubElement(termCompGrp_struct_l2, "termComp").text = word
                # <termNote type="partOfSpeech">noun</termNote>
                etree.SubElement(termCompGrp_struct_l2, "termNote",
                type="partOfSpeech").text = pos_internal_l2[i]
#############################################



        for n,v in enumerate(field_5_variants_l1,1):
            # <termNote type="variant01">déinos con anse ad anello</termNote>
            v_num = str(n).zfill(2)
            etree.SubElement(parent_node_l1, "termNote", type="variant{}".format(v_num)).text = v
        for n,s in enumerate(field_6_synonyms_l1,1):
            # <termNote type="variant01">déinos con anse ad anello</termNote>
            s_num = str(n).zfill(2)
            etree.SubElement(parent_node_l1, "termNote", type="synonym{}".format(s_num)).text = s
        for n,h in enumerate(field_8_hyper_l1,1):
            # <termNote type="hypernyms01">Contenitori e recipienti</termNote>
            h_num = str(n).zfill(2)
            etree.SubElement(parent_node_l1, "termNote", type="hypernyms{}".format(h_num)).text = h


        
        for n,v in enumerate(field_5_variants_l2,1):
            # <termNote type="variant01">déinos con anse ad anello</termNote>
            v_num = str(n).zfill(2)
            etree.SubElement(parent_node_l2, "termNote", type="variant{}".format(v_num)).text = v
        for n,s in enumerate(field_6_synonyms_l2,1):
            # <termNote type="variant01">déinos con anse ad anello</termNote>
            s_num = str(n).zfill(2)
            etree.SubElement(parent_node_l2, "termNote", type="synonym{}".format(s_num)).text = s
        for n,h in enumerate(field_8_hyper_l2,1):
            # <termNote type="hypernyms01">Contenitori e recipienti</termNote>
            h_num = str(n).zfill(2)
            etree.SubElement(parent_node_l2, "termNote", type="hypernyms{}".format(h_num)).text = h

    tbx_string = etree.tostring(
        root,
        pretty_print=True,
        xml_declaration=True,
        doctype='<!DOCTYPE martif SYSTEM "TBXcoreStructV02.dtd">', # --> verify
        encoding='UTF-8'
    )

    return tbx_string

if __name__ == '__main__':

    tbx_string = csv2tbx(
        input_l1='../../glossario_it.csv',
        input_l2='../../glossario_en.csv',
        lang1 = 'it',
        lang2='en',
        subjectField="Archaeology", 
        id_prefix = 'RA',
        ontology_link='http://www.cidoc-crm.org/cidoc-crm', 
        ontology_name='CIDOC CRM'
    )


    with open("../data/output.tbx", "wb") as f_out:
        f_out.write(tbx_string)


