'''
# Description
Functions to read and manipulate text.

# Index
- `find_pos()`
- `find_pos_regex`
- `find()`
- `replace()`
- `replace_line()`
- `insert_under()`
- `replace_under()`
- `delete_under()`
- `replace_between()`
- `delete_between()`
- `correct_with_dict()`

---
'''


from .file import *
import mmap
import re


def find_pos(keyword:str, file, number_of_matches:int=0) -> list:
    '''
    Returns a list of the positions of a `keyword` in a given `file`.\n
    The value `number_of_matches` specifies the max number of matches to return.
    Defaults to 0 to return all possible matches. Set it to 1 to return only one match,
    or to negative integers to start searching from the end of the file upwards.\n
    This method is faster than `find_pos_regex()`, but does not search for regular expressions.
    '''
    file_path = get(file)
    positions = []
    with open(file_path, 'r+b') as f:
        mm = mmap.mmap(f.fileno(), length=0, access=mmap.ACCESS_READ)
    keyword_bytes = keyword.encode()
    if number_of_matches >= 0:
        start = 0
        while number_of_matches == 0 or len(positions) < number_of_matches:
            pos = mm.find(keyword_bytes, start)
            if pos == -1:
                break
            end = pos + len(keyword_bytes)
            positions.append((pos, end))
            start = end
    else:
        start = len(mm)
        while len(positions) < abs(number_of_matches):
            pos = mm.rfind(keyword_bytes, 0, start)
            if pos == -1:
                break
            end = pos + len(keyword_bytes)
            positions.append((pos, end))
            start = pos
        positions.reverse()
    return positions


def find_pos_regex(keyword:str, file, number_of_matches:int=0) -> list:
    '''
    Returns a list of the positions of a `keyword` in a given `file`.\n
    The value `number_of_matches` specifies the max number of matches to return.
    Defaults to 0 to return all possible matches. Set it to 1 to return only one match,
    or to negative integers to start searching from the end of the file upwards.\n
    This method is slower than `find_pos()`, but it can search for regular expressions.
    '''
    file_path = get(file)
    positions = []
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    if number_of_matches > 0:
        start = 0
        while len(positions) < number_of_matches:
            match = re.search(keyword, content[start:])
            if not match:
                break
            match_start = start + match.start()
            match_end = start + match.end()
            positions.append((match_start, match_end))
            start = match_end
    else:
        all_matches = list(re.finditer(keyword, content))
        if number_of_matches == 0:
            positions = [(match.start(), match.end()) for match in all_matches]
        else:
            positions = [(match.start(), match.end()) for match in all_matches[-abs(number_of_matches):]]
    return positions


def find(keyword:str,
         file:str,
         number_of_matches:int=0,
         additional_lines:int=0,
         split_additional_lines: bool=False,
         regex:bool=False) -> list:
    '''
    Finds the line(s) containing the `keyword` string in the given `file`,
    returning a list with the matches.\n
    The value `number_of_matches` specifies the max number of matches to be returned.
    Defaults to 0 to return all possible matches. Set it to 1 to return only one match,
    or to negative integers to start the search from the end of the file upwards.\n
    The value `additional_lines` specifies the number of additional lines
    below the target line that are also returned;
    2 to return the found line plus two additional lines below, etc.
    Negative values return the specified number of lines before the target line.
    The original ordering from the file is preserved.
    Defaults to `additional_lines=0`, only returning the target line.
    By default, the additional lines are returned in the same list item as the match separated by a `\\n`,
    unless `split_additional_lines=True`, in which case they are added as additional items in the list.\n
    To use regular expressions in the search, set `regex=True`.
    By default regex search is deactivated, using the faster mmap.find and rfind methods instead.
    '''
    file_path = get(file)
    matches = []
    if regex:
        positions = find_pos_regex(keyword, file, number_of_matches)
    else:
        positions = find_pos(keyword, file, number_of_matches)
    with open(file_path, 'r+b') as f:
        mm = mmap.mmap(f.fileno(), length=0, access=mmap.ACCESS_READ)
    for start, end in positions:
        # Get the positions of the full line containing the match
        line_start = mm.rfind(b'\n', 0, start) + 1
        line_end = mm.find(b'\n', start, len(mm)-1)
        # Default values for the start and end of the line
        if line_start == -1: line_start = 0
        if line_end == -1: line_end = len(mm) - 1
        # Adjust the line_end to add additional lines after the match
        match_start = line_start
        match_end = line_end
        if additional_lines > 0:
            for _ in range(abs(additional_lines)):
                match_end = mm.find(b'\n', match_end + 1, len(mm)-1)
                if match_end == -1:
                    break
        elif additional_lines < 0:
            for _ in range(abs(additional_lines)):
                match_start = mm.rfind(b'\n', 0, match_start - 1) + 1
                if match_start == -1:
                    break
        # Save the matched lines
        matches.append(mm[match_start:match_end].decode())
    if split_additional_lines:
        splitted_matches = []
        for string in matches:
            splitted_match = string.splitlines()
            splitted_matches.extend(splitted_match)
        matches = splitted_matches
    return matches


def replace(text:str, keyword:str, file:str, number_of_replacements:int=0) -> None:
    '''
    Replaces the `keyword` string with the `text` string in the given `filename`.
    The value `number_of_replacements` specifies the number of replacements to perform:
    1 to replace only the first keyword found, 2, 3...
    Use negative values to replace from the end of the file,
    eg. to replace the last found key, use `number_of_replacements = -1`.
    To replace all values, set `number_of_replacements = 0`, which is the value by default.
    ```
    line... keyword ...line -> line... text ...line
    ```
    '''
    file_path = get(file)
    with open(file_path, 'r+') as f:
        content = f.read()
        if number_of_replacements == 0:
            content = content.replace(keyword, text)
        else:
            replacements_left = abs(number_of_replacements)
            while replacements_left > 0:
                if number_of_replacements > 0: # If negative, start backwards
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


def replace_line(text: str, keyword: str, file: str, number_of_replacements:int=0) -> None:
    '''
    Replaces the entire line containing the `keyword` string with the `text` string in the given `filename`.
    The value `number_of_replacements` specifies the number of lines to replace:
    1 to replace only the first line with the keyword, 2, 3...
    Use negative values to replace from the end of the file,
    e.g., to replace only the last line containing the keyword, use `number_of_replacements = -1`.
    To replace all lines, set `number_of_replacements = 0`, which is the value by default.
    '''
    file_path = get(file)
    with open(file_path, 'r+') as f:
        lines = f.readlines()
        if number_of_replacements == 0:
            lines = [line.replace(keyword, text) for line in lines]
        else:
            replacements_left = abs(number_of_replacements)
            step = 1 if number_of_replacements > 0 else -1
            start = 0 if number_of_replacements > 0 else len(lines) - 1
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
    > TODO: IN THE FUTURE SHOULD BE POSITION-AGNOSTIC. The keyword currently must be at the beginning of the line.
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
    > TODO: IN THE FUTURE SHOULD BE POSITION-AGNOSTIC
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


def correct_with_dict(file:str, fixing_dict:dict) -> None:
    '''
    Corrects the given text `file` using the `fixing_dict` dictionary.
    '''
    file_path = get(file)

    with open(file_path, 'r+') as f:
        content = f.read()
        for key, value in fixing_dict.items():
            content = content.replace(key, value)
        f.seek(0)
        f.write(content)
    return None

