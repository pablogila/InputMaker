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


def number(text:str, name:str='') -> float:
    '''
    Extracts the float value of a given `name` variable from a raw `text`.
    '''
    if text == None:
        return None
    pattern = re.compile(rf"{name}\s*=?\s*(-?\d+(?:\.\d+)?(?:[eE][+\-]?\d+)?)")
    match = pattern.search(text)
    if match:
        return float(match.group(1))
    return text
    

def string(text:str, name:str, remove_commas:bool=False) -> str:
    '''
    Extracts the `text` value of a given `name` variable from a raw string.
    If `remove_commas=True` and the value is between commas, it is returned without said commas.
    By default, `remove_commas=False`.\n
    Example:
    ```
    " blabla name = 'value' "
    > 'value'
    ```
    > TO - FIX
    '''
    pattern = re.compile(rf"{name}\s*(:|=)?\s*['\"](.*?)(?=['\"]|$).*")
    match = re.search(pattern, text)
    if match:
        value = match.group(1)
        if remove_commas:
            value = value.strip(",")
        return value
    return text


def column(text:str, column:int) -> float:
    '''
    Extracts the desired float `column` of a given `string`.
    '''
    if text is None:
        return None
    columns = text.split()
    pattern = r'(-?\d+(?:\.\d+)?(?:[eE][+\-]?\d+)?)'
    if column < len(columns):
        match = re.match(pattern, columns[column])
        if match:
            return float(match.group(1))
    return text

