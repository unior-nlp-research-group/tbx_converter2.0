
def guess_encoding(rawdata):
    import chardet
    confidence_encoding_scores = chardet.detect(rawdata)    
    if confidence_encoding_scores:
        return confidence_encoding_scores['encoding']
    raise UnicodeDecodeError

def check_encoding(rawdata, encoding='utf-8'):
    import codecs
    try:
        codecs.decode(rawdata, encoding)
    except UnicodeDecodeError:
        return False
    return True

def check_file_encoding(filename, encoding='utf-8'):
    import codecs
    try:
        f = codecs.open(filename, encoding=encoding, errors='strict')
        for line in f:
            pass
        return True
    except UnicodeDecodeError:
        return False

def flatten(L):
    ret = []
    for i in L:
        if isinstance(i,list):
            ret.extend(flatten(i))
        else:
            ret.append(i)
    return ret
    
def escape_markdown(text):
    for char in '*_`[':
        text = text.replace(char, '\\'+char)
    return text

def containsMarkdown(text):
    for char in '*_`[':
        if char in text:
            return True
    return False


if __name__ == "__main__":
    pass