from unidecode import unidecode
import re


def cleanse(s):
    pattern = r'[%$\\]'
    ascii_s = unidecode(s)
    s_without_special_chars = re.sub(pattern, '', ascii_s)
    s_with_escape_chars = s_without_special_chars.replace("'", r'\'')
    return s_with_escape_chars

def clean_latex(text):
    # Replace specific LaTeX commands with readable text
    text = re.sub(r'\$\sim(\d+)\%$', r'approximately \1%', text)
    
    # Generic removal of other LaTeX commands (optional, customize as needed)
    text = re.sub(r'\$[^$]*\$', '', text)
    
    return text