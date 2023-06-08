import re

def SanitiseData(string):
    '''First attempt. Unresolved'''
    if not re.match(r'^[a-zA-Z0-9_ -]+$', string):
        raise ValueError("Invalid sequence string: " + string)
    else:
        return string