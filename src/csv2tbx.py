from lxml import etree
import csv

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

def csv2tbx(lines, lang, subjectField, id_prefix, uri_target=None, uri_name=None):

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

    csv_reader = csv.reader(lines, delimiter=';')        
    for n,row in enumerate(csv_reader,1):
        if len(row) == 2:
            # assume first field term and second pos and the other empty
            row.extend(['']*7)
        if len(row) != 9:
            error_msg = "Error in input CSV: line {} has {} fields instead of 9".format(n, len(row))
            raise CsvFormatError(error_msg)
        row = [x.strip() for x in row]
        field_1_term = row[0]
        field_2_pos_upper = row[1].upper()
        field_3_mw_pos_upper = row[2].upper()
        field_4_flex_lower = row[3].lower()
        field_5_variants = [x.strip() for x in row[4].split(',') if x]
        field_6_synonyms = [x.strip() for x in row[5].split(',') if x]
        field_7_desc = row[6]
        field_8_hyper = [x.strip() for x in row[7].split(',') if x]
        field_9_class = row[8]
        use_ntig = field_3_mw_pos_upper

        pos_full = POS_MAPPING.get(field_2_pos_upper, POS_MAPPING_OTHER)
        gender_full, number_full = None, None
        if field_4_flex_lower:
            if len(field_4_flex_lower)!=4:
                error_msg = "Error in input CSV: line {} has error in field 4 ({}): \
                    inflection should be 4 characters long (e.g., ms+-)".format(n, field_4_flex_lower)
                raise CsvFormatError(error_msg)
            if field_4_flex_lower[0] not in ['m','f']:
                error_msg = "Error in input CSV: line {} has error in field 4 ({}): \
                    first character should be m (masculine) or f (feminine)".format(n, field_4_flex_lower)
                raise CsvFormatError(error_msg)
            if field_4_flex_lower[1] not in ['s','p']:
                error_msg = "Error in input CSV: line {} has error in field 4 ({}): \
                    second character should be s (singular) or p (plural)".format(n, field_4_flex_lower)
                raise CsvFormatError(error_msg)
            gender_full = 'masculine' if field_4_flex_lower[0]=='m' else 'feminine'
            number_full = 'singular' if field_4_flex_lower[1]=='s' else 'plural'

        # term is multi word if first field has spaces and third field (interal structure) is present
        use_ntig = ' ' in field_1_term and field_3_mw_pos_upper 

        id_str = "{}_{}".format(id_prefix, n)
        # <termEntry id="RA_286">
        termEntry_struct = etree.SubElement(body_struct, "termEntry", id=id_str)
        descripGrp_struct = etree.SubElement(termEntry_struct, "descripGrp")
        # <descrip type="subjectField">Archaeology</descrip> 
        etree.SubElement(descripGrp_struct, "descrip", type="subjectField").text = subjectField
        if field_7_desc:
            # <descrip type="definition">Definition Text</descrip>
            etree.SubElement(descripGrp_struct, "descrip", type="definition").text = field_7_desc
        # <xref type="URI" target= "http://www.cidoc-crm.org/cidoc-crm">CIDOC CRM Ontology</xref>
        etree.SubElement(descripGrp_struct, "xref", type="URI", target=uri_target).text = '{} {}'.format(uri_name, 'Ontology')                
        # <langSet xml:lang="it">
        langSet_struct = etree.SubElement(body_struct, "langSet") #attrib={'xml:lang':lang}
        attr = langSet_struct.attrib
        attr['{http://www.w3.org/XML/1998/namespace}lang'] = lang
        
        ntig_tig_struct_tag = "ntig" if use_ntig else "tig"
        ntig_tig_struct = etree.SubElement(langSet_struct, ntig_tig_struct_tag)

        if use_ntig:
            field_1_words = row[0].split() # lista di parole      
            pos_internal = [POS_MAPPING.get(x, POS_MAPPING_OTHER) for x in field_3_mw_pos_upper]          

            termGrp_struct = etree.SubElement(ntig_tig_struct, "termGrp")
            parent_node = termGrp_struct
        else:
            parent_node = ntig_tig_struct


        # <term>dinos con anse ad anello</term>
        etree.SubElement(parent_node, 'term').text = row[0]
        # <termNote type="termType">fullForm</termNote>
        etree.SubElement(parent_node, 'termNote', type="termType").text = 'fullForm'
        # <termNote type="partOfSpeech">noun</termNote>
        etree.SubElement(parent_node, 'termNote', type="partOfSpeech").text = pos_full
        if gender_full and number_full:
            # <termNote type="grammaticalGender">masculine</termNote>
            etree.SubElement(parent_node, 'termNote', type="grammaticalGender").text = gender_full
            # <termNote type="grammaticalNumber">singular</termNote>
            etree.SubElement(parent_node, 'termNote', type="grammaticalNumber").text = number_full
        # <xref type="URI" target="http://www.cidoc-crm.org/cidoc-crm/E22">CIDOC CRM Class</xref>
        uri_target_term = '{}/{}'.format(uri_target, field_9_class)
        etree.SubElement(parent_node, "xref", type="URI", target=uri_target_term).text = '{} {}'.format(uri_name, 'Class')                

        if use_ntig:
            # <termCompList type="lemma">
            termCompList_struct = etree.SubElement(parent_node, "termCompList", type="lemma")
            for i, word in enumerate(field_1_words):
                termCompGrp_struct = etree.SubElement(termCompList_struct, "termCompGrp")
                # <termComp>dinos</termComp>
                etree.SubElement(termCompGrp_struct, "termComp").text = word
                # <termNote type="partOfSpeech">noun</termNote>
                etree.SubElement(termCompGrp_struct, "termNote", type="partOfSpeech").text = pos_internal[i]

        for n,v in enumerate(field_5_variants,1):
            # <termNote type="variant01">déinos con anse ad anello</termNote>
            v_num = str(n).zfill(2)
            etree.SubElement(parent_node, "termNote", type="variant{}".format(v_num)).text = v
        for n,s in enumerate(field_6_synonyms,1):
            # <termNote type="variant01">déinos con anse ad anello</termNote>
            s_num = str(n).zfill(2)
            etree.SubElement(parent_node, "termNote", type="synonym{}".format(s_num)).text = s
        for n,h in enumerate(field_8_hyper,1):
            # <termNote type="hypernyms01">Contenitori e recipienti</termNote>
            h_num = str(n).zfill(2)
            etree.SubElement(parent_node, "termNote", type="hypernyms{}".format(h_num)).text = h

    tbx_string = etree.tostring(
        root,
        pretty_print=True,
        xml_declaration=True,
        doctype='<!DOCTYPE martif SYSTEM "TBXcoreStructV02.dtd">', # --> verify
        encoding='UTF-8'
    )

    return tbx_string

if __name__ == '__main__':
    with open('../data/input.csv') as f_in:
        lines = f_in.readlines()

    tbx_string = csv2tbx(
        lines = lines,
        lang = 'it',
        subjectField="Archaeology", 
        id_prefix = 'RA',
        uri_target='http://www.cidoc-crm.org/cidoc-crm', 
        uri_name='CIDOC CRM'
    )

    with open("../data/output.tbx", "wb") as f_out:
        f_out.write(tbx_string)


