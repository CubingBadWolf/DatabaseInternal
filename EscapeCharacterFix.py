import re

def SanitiseData(string):
    '''First attempt. Unresolved'''
    invalid_chars = r'[^A-Za-z0-9_ ]+'
    return re.sub(invalid_chars,r'\\\1', string)