import re

def SanitiseData(string):
    '''First attempt. Unresolved'''
    if not re.match(r'^[a-zA-Z0-9_ ]+$', string): #-s? often used for injection comments, but double barrels?
        raise ValueError("Invalid sequence string: " + string)
    else:
        return string