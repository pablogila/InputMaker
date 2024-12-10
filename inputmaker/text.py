'''
# Description
Common functions to manipulate text by using keywords.

# Index
- `replace()`
- `replace_line()`
- `insert_under()`
- `replace_under()`
- `delete_under()`
- `replace_between()`
- `delete_between()`

---
'''


from .file import *


def replace(text:str, keyword:str, file:str, replacements:int=0) -> None:
    '''
    Replaces the `keyword` string with the `text` string in the given `filename`.
    The value `replacements` specifies the number of replacements to perform:
    1 to replace only the first keyword found, 2, 3...
    Use negative values to replace from the end of the file,
    eg. to replace the last found key, use `replacements = -1`.
    To replace all values, set `replacements = 0`, which is the value by default.
    ```
    line... keyword ...line -> line... text ...line
    ```
    '''
    file_path = get(file)
    with open(file_path, 'r+') as f:
        content = f.read()
        if replacements == 0:
            content = content.replace(keyword, text)
        else:
            replacements_left = abs(replacements)
            while replacements_left > 0:
                if replacements > 0:
                    index = content.find(keyword)
                else:
                    index = content.rfind(keyword)
                if index == -1:
                    break
                content = "".join([content[:index], text, content[index + len(keyword):]])
                replacements_left -= 1
        f.seek(0)
        f.write(content)
        f.truncate()


def replace_line(text: str, keyword: str, file: str, replacements: int = 0) -> None:
    """
    Replaces the entire line containing the `keyword` string with the `text` string in the given `filename`.
    The value `replacements` specifies the number of lines to replace:
    1 to replace only the first line with the keyword, 2, 3...
    Use negative values to replace from the end of the file,
    e.g., to replace only the last line containing the keyword, use `replacements = -1`.
    To replace all lines, set `replacements = 0`, which is the value by default.
    """
    file_path = get(file)
    with open(file_path, 'r+') as f:
        lines = f.readlines()
        if replacements == 0:
            lines = [line.replace(keyword, text) for line in lines]
        else:
            replacements_left = abs(replacements)
            step = 1 if replacements > 0 else -1
            start = 0 if replacements > 0 else len(lines) - 1
            while replacements_left > 0:
                if step > 0:
                    for i in range(start, len(lines)):
                        if keyword in lines[i]:
                            lines[i] = text + '\n'
                            replacements_left -= 1
                            break
                else:
                    for i in range(start, -1, -1):
                        if keyword in lines[i]:
                            lines[i] = text + '\n'
                            replacements_left -= 1
                            break
                start += step
        f.seek(0)
        f.writelines(lines)
        f.truncate()


def insert_under(text:str, keyword:str, file:str, only_first=False) -> None:
    '''
    Inserts the given `text` string under the first occurrence
    of the `keyword` in the given `file`.
    The keyword can be at any position within the line.
    If `only_first=True`, it will only work
    at the first instance of the keyword, ignoring the rest.
    The keyword can be at any position in the line, not just at the beginning.
    ```
    line1
    keyword line2
    text
    line3
    ```
    '''
    file_path = get(file)
    with open(file_path, 'r') as f:
        document = f.readlines()
    indices = (i for i, line in enumerate(document) if keyword in line.strip())
    if indices:
        if only_first:
            document.insert(indices[0] + 1, text + "\n")
        else:
            for index in indices:
                document.insert(index + 1, text + "\n")
        with open(file_path, 'w') as f:
            f.writelines(document)
    else:
        raise ValueError("Didn't find the '" + keyword + "' keyword in " + file_path)
    return None


def replace_under(text:str, keyword:str, file:str) -> None:
    '''
    Replaces the lines under the first occurrence of the `keyword`
    in the given `filename` with the given `text` string.
    > TO-DO: IN THE FUTURE SHOULD BE POSITION-AGNOSTIC. The keyword currently must be at the beginning.
    ```
    line1
    keyword line2
    text
    line4
    ```
    '''
    file_path = get(file)
    with open(file_path, 'r') as f:
        document = f.readlines()
    index = next((i for i, line in enumerate(document) if line.strip().startswith(keyword)), None)
    if index is not None:
        for i, row in enumerate(text):
            if index + 1 + i < len(document):
                document[index + 1 + i] = row + "\n"
        with open(file_path, 'w') as f:
            file.writelines(document)
    else:
        raise ValueError("Didn't find the '" + keyword + "' keyword in " + file_path)
    return None


def delete_under(keyword:str, file:str) -> None:
    '''
    Deletes the lines under the first occurrence of the `keyword` in the given `file`.
    > TO-DO: IN THE FUTURE SHOULD BE POSITION-AGNOSTIC
    ```
    lines...
    keyword
    (end of file)
    ```
    '''
    file_path = get(file)
    with open(file_path, 'r') as f:
        lines = f.readlines()
    keep = []
    for line in lines:
        if keyword in line:
            break
        else:
            keep.append(line)
    with open(file, 'w') as f:
        f.writelines(keep)
    return None


def replace_between(text:str, key1:str, key2:str, file:str) -> None:
    '''
    Replace lines with a given `text`, between the keywords `key1` and `key2`,
    in a given `file`.
    ```
    lines...
    key1
    text
    key2
    lines...
    ```
    '''
    delete_between(key1, key2, file)
    insert_under(text, key1, file)
    return None


def delete_between(key1:str, key2:str, file:str) -> None:
    '''
    Deletes the lines between two keywords in a given `file`.
    ```
    lines...
    key1
    (lines to be deleted)
    key2
    lines...
    ```
    '''
    file_path = get(file)
    with open(file_path, 'r') as f:
        lines = f.readlines()
    keep = []
    skip = False
    for line in lines:
        if key1 in line:
            skip = True
        if key2 in line:
            skip = False
        if not skip or key1 in line:
            keep.append(line)
    with open(file_path, 'w') as f:
        f.writelines(keep)
    return None

