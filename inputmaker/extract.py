'''
# Description
Functions to extract data from raw text strings.

WARNING: These functions are yet to be properly implemented.

# Index
- `number()`
- `string()`
- `column()`

---
'''


import re


def number(string:str, name:str) -> float:
    '''
    Extracts the float value of a given `name` variable from a raw `string`.
    '''
    if string == None:
        return None
    pattern = re.compile(name + r'\s*=?\s*(-?\d+(?:\.\d+)?(?:[eE][+\-]?\d+)?)')
    match = pattern.search(string)
    if match:
        return float(match.group(1))
    else:
        return None
    

def string(string:str, name:str, remove_commas:bool=False) -> str:
    '''
    Extracts the `string` value of a given `name` variable from a raw string.
    If `remove_commas=True` and the value is between commas, it is returned without said commas.
    By default, `remove_commas=False`.
    '''
    if string == None:
        return None
    if remove_commas:
        pattern = re.compile(name + r"\s*(=)?\s*['\"](.*?)(?=['\"]|$)")
        match = pattern.search(string)
        if match:
            return match.group(2).strip()
    else:
        pattern = re.compile(name + r"\s*=\s*(\S.*)?$")
        match = pattern.search(string)
        if match:
            return match.group(1).strip()
    if not match:
        return None


def column(string:str, column:int) -> float:
    '''
    Extracts the desired float `column` of a given `string`.
    '''
    if string is None:
        return None
    columns = string.split()
    pattern = r'(-?\d+(?:\.\d+)?(?:[eE][+\-]?\d+)?)'
    if column < len(columns):
        match = re.match(pattern, columns[column])
        if match:
            return float(match.group(1))
    return None

