# General information

In this repository we provide **CSV2TBX** a tool for **converting CSV Linguistic Resources into TBX format**.\
This tool is available on Telegram as a ChatBot under the name [CSV2TBX](https://t.me/CSV2TBX_bot). \
**CSV2TBX** fully supports multilingual datasets, as it takes as input one CSV file per language and gives as output a TBX file, the standard TermBase eXchange format for terminology management and sharing. The converter also supports the integration of ontology references.

# Conversion process
At the start of the process, the converter will ask whether the user is working with one or more languages. In case the user is working with more than one languages, it will ask to enter the [**ISO Language Code**](http://www.lingoes.net/en/translator/langcode.htm) for each language separated by a comma using (e.g. ‘it, en’). 

After that, the user can upload the .csv file to be converted into TBX.

**Please remember that the order in which the CSV files are sent has to be the same order in which the languages were typed (e.g if the input for the selected languages was ‘it, en’, the user should send the Italian CSV file first, then the English one)**.

# Input File
Each monolingual CSV file should contain 9 fields separated by 8 semicolons (;) per line.\
In case of multiple multilingual CSV files, each row should refer to the same item.\
In case one language doesn’t have an entry for that specific item, be careful to leave the row for that item empty in the CSV file for that language.

1. **Term*** is mandatory and must contain the term (which could be a single word or a multiword expression (MWE), e.g., column krater, antefixes, etc.
1. **POS tag***, is mandatory and must contain the Part of Speech tag of the entry, e.g., N, P, A, etc.
1. **Internal POS** tags can contain the POS of MWE’s single components, e.g., NN etc.
1. **Grammatical info** should contain the gender and number of the term, in the format ns-+
1. **Variants** can host all orthographic variants of a term, e.g., column krater,column-krater
1. **Synonyms** should contain the synonyms for the selected term. If more than one Synonym is available they can be listed separated by comma, as for Variants.
1. **Definition** is the field dedicated to a brief explication of the term like a dictionary gloss, e.g., Kraters with columnlike handles extending from the shoulders to the rim. The feet are echinus shaped. This vessel type was especially popular in black-figure.
1. **Hypernyms** can contain hierarchically higher and more general lexical entries comprising the term e.g., architectural elements.
1. **Ontology class** reference can host the term’s corresponding ontology class in a reference domain ontology such as CIDOC CRM Ontology for Cultural Heritage domain e.g., E22_Man-Made_Object

*Mandatory fields. If some of the optional fields are missing, the separator has to be inserted to preserve the number of expected fields.

**Example of CSV input file**
```csv
column krater;N;NN;ns-+;column crater,column-krater;;Kraters with columnlike handles extending from the shoulders to the rim. The feet are echinus shaped. This vessel type was especially popular in black-figure.;vessel and containers,furnishings and equipment;E22_Man-Made_Object
antefix;N;;ns-+;antefixae;Ornaments at the ridge or eaves of a roof, in classical architecture and derivatives, that close or conceal the open end of a row of cover tiles.;architectural elements;E22_Man-Made_Object
```

# Output file
The converter output is a TBX file as defined by the ISO 30042:2008 standard (TBX v2), employing the DatCatInfo categories in the DCA style. Note that TBX v2 allows the use of the <ntig> element for MWE decomposition.

**Example of monolingual TBX output file**
```
<text>
    <body>
      <termEntry id="AR_1">
        <descripGrp>
          <descrip type="subjectField">Archaeology</descrip>
          <descrip type="definition">Kraters with columnlike handles extending from the shoulders to the rim. The feet are echinus shaped. This vessel type was especially popular in black-figure.</descrip>
          <xref type="URI"target="http://www.cidoc-crm.org/cidoc-crm">CIDOC CRM Ontology</xref>
        </descripGrp>
      </termEntry>
      <langSet xml:lang="en">
        <ntig>
          <termGrp>
            <term>column krater</term>
            <termNote type="termType">fullForm</termNote>
            <termNote type="partOfSpeech">noun</termNote>
            <termNote type="grammaticalGender">neuter</termNote>
            <termNote type="grammaticalNumber">singular</termNote>
            <xref type="URI"target="http://www.cidoc-crm.org/cidoc-crm/E22_Man-Made_Object">CIDOC CRM Class</xref>
            <termCompList type="lemma">
              <termCompGrp>
                <termComp>column</termComp>
                <termNote type="partOfSpeech">noun</termNote>
              </termCompGrp>
              <termCompGrp>
                <termComp>krater</termComp>
                <termNote type="partOfSpeech">noun</termNote>
              </termCompGrp>
            </termCompList>
            <termNote type="variant01">column crater</termNote>
            <termNote type="variant02">column-krater</termNote>
            <termNote type="hypernyms01">vessel and containers</termNote>            
           <termNote type="hypernyms02">furnishings and equipment</termNote>
          </termGrp>
        </ntig>
      </langSet>
      <termEntry id="AR_2">
        <descripGrp>
          <descrip type="subjectField">Archaeology</descrip>
          <descrip type="definition">Ornaments at the ridge or eaves of a roof, in classical architecture and derivatives, that close or conceal the open end of a row of cover tiles.</descrip>
          <xref type="URI" 
           target="http://www.cidoc-crm.org/cidoc-crm">CIDOC CRM Ontology</xref>
        </descripGrp>
      </termEntry>
      <langSet xml:lang="en">
        <tig>
          <term>antefix</term>
          <termNote type="termType">fullForm</termNote>
          <termNote type="partOfSpeech">noun</termNote>
          <termNote type="grammaticalGender">neuter</termNote>
          <termNote type="grammaticalNumber">singular</termNote>
          <xref type="URI"target="http://www.cidoc-crm.org/cidoc-crm/E22_Man-Made_Object"> CIDOC CRM Class</xref>
          <termNote type="variant01">antefixae</termNote>
          <termNote type="hypernyms01">architectural elements</termNote>
        </tig>
      </langSet>
    </body>
  </text>
```

**Example of bilingual TBX output file**
```  <text>
    <body>
      <termEntry id="AR_1">
        <descripGrp>
          <descrip type="subjectField">archaeology</descrip>
          <xref type="URI" target="http://www.cidoc-crm.org/cidoc-crm">cidoc crm Ontology</xref>
        </descripGrp>
        <langSet xml:lang="it">
          <descrip type="definition">Piccoli vasi di svariate fogge e materiali (soprattutto paste vitree) destinati presso i popoli antichi a contenere sostanze aromatiche</descrip>
          <tig>
            <term>balsamario</term>
            <termNote type="termType">fullForm</termNote>
            <termNote type="partOfSpeech">noun</termNote>
            <xref type="URI" target="http://www.cidoc-crm.org/cidoc-crm/E23">cidoc crm 
                        Class</xref>
          </tig>
        </langSet>
        <langSet xml:lang="en">
          <descrip type="definition">Containers probably used to hold ointments and perfume. Early ceramic examples found at Petra (probably 4th-century BCE) were in the typical Hellenistic form of the spindle bottle, but this form was later completely replaced by a series of high-necked types with round to ovoid bodies of varying and apparently standardized forms (from the 1st century BCE onwards). The number of unguentaria found at Petra suggests that they were made locally; their manufacture would have been linked to the myrrh and other unguents that the Nabataeans traded. They have also been found at western sites. Pear-shaped glass unguentaria were later made at various locations in the Arabian peninsula.</descrip>
          <tig>
            <term>unguentarium</term>
            <termNote type="termType">fullForm</termNote>
            <termNote type="partOfSpeech">noun</termNote>
            <xref type="URI" target="http://www.cidoc-crm.org/cidoc-crm/E23">cidoc crm 
                        Class</xref>
          </tig>
        </langSet>
      </termEntry>
```


# License and Citation
The tool has been developed by the [**UNIOR NLP Research Group**](https://sites.google.com/view/unior-nlp-research-group) L'Orientale University of Naples.
 **Contact**: uniornlp@gmail.com\
The tool is released under **CC license**.\
To cite this work, please use:
```latex
@inproceedings{speranza2019from,
title={From Linguistic Resources to Ontology-Aware Terminologies:Minding the Representation Gap},
author={Speranza, Giulia and di Buono, Maria Pia and Monti, Johanna and Sangati, Federico},
booktitle={International Conference on Language Resources and Evaluation. LREC2020},
year={2020}
}
```
