'''
# Description
Common functions to manipulate input files with custom keywords.

# Index
- `get_file()`
- `get_files_from_folder()`
- `get_file_from_folder()`
- `rename_files()`
- `rename_files_on_subfolders()`
- `copy_files_to_subfolders()`
- `copy_to_newfile()`
- `template_to_newfile()`
- `replace_str_on_keyword()`
- `replace_line_with_keyword()`
- `insert_lines_under_keyword()`
- `replace_lines_under_keyword()`
- `delete_lines_under_keyword()`
- `replace_lines_between_keywords()`
- `delete_lines_between_keywords()`
- `correct_file_with_dict()`

---
'''


import os


def get_file(file:str):
    '''
    Check if the given `file` exists, and returns its full path.
    If the file does not exist in the provided path,
    it will check in the current working directory.
    If the file is still missing, it raises an error.
    '''
    if os.path.isfile(file):
        return file
    elif os.path.isfile(os.path.join(os.getcwd(), file)):
        return os.path.join(os.getcwd(), file)
    raise FileNotFoundError('Missing file at ' + file + ' or in the CWD ' + os.getcwd())


def get_files_from_folder(folder:str, extensions=None) -> list:
    '''
    Returns a list with the files in a given `folder`.
    If the folder does not exist in the given path,
    it checks in the current working directory.
    If the folder is still missing, it raises an error.

    If `extensions` is provided, it returns only the files
    with the specified extension/s (string or list with strings).
    '''
    if os.path.isdir(folder):
        files = os.listdir(folder)
    elif os.path.isdir(os.path.join(os.getcwd(), folder)):
        files = os.listdir(os.path.join(os.getcwd(), folder))
    else:
        raise FileNotFoundError('Missing folder at ' + folder + ' or in the CWD ' + os.getcwd())
    if extensions is None:
        return files
    else:
        target_files = []
        if not isinstance(extensions, list):
            extensions = [extensions]
        for extension in extensions:
            for file in files:
                if file.endswith(extension):
                    target_files.append(file)
        return target_files


def get_file_from_folder(folder:str, extensions=None, preferred_file:str=None):
    '''
    Returns the first file with the given `extension` (str or list of strings)
    in the given `folder`.
    If `preferred_file` is provided and found, it will return that file.
    '''
    files = get_files_from_folder(folder, extensions)
    if preferred_file in files:
        return preferred_file
    elif files:
        return files[0]
    else:
        return None


def rename_files(old_string:str, new_string:str) -> None:
    '''
    Renames files in the current working directory,
    replacing the `old_string` by the `new_string`.
    '''
    for file in os.listdir('.'):
        if old_string in file:
            os.rename(file, file.replace(old_string, new_string))
    return None


def rename_files_on_subfolders(old_extension:str, new_extension:str) -> None:
    '''
    Renames the files inside the subfolders in the current working directory,
    from an `old_extension` to the `new_extension`.
    '''
    for folder in os.listdir('.'):
        if os.path.isdir(folder):
            for file in os.listdir(folder):
                if file.endswith(old_extension):
                    old_file = os.path.join(folder, file)
                    new_file = os.path.join(folder, file.replace(old_extension, new_extension))
                    os.rename(old_file, new_file)
    return None


def copy_files_to_subfolders(extension:str, words_to_delete=[]) -> None:
    '''
    Copies the files with the given `extension` to individual subfolders.
    Runs in the current working directory.
    '''
    path = os.getcwd()
    old_files = get_files_from_folder(path, extension)
    if old_files is None:
        raise ValueError('No ' + extension + ' files found in path!')
    for old_file in old_files:
        new_file = old_file
        for word in words_to_delete:
            new_file = new_file.replace(word, '')
        folder = new_file.replace(extension, '')
        os.makedirs(folder)
        new_file_path = folder + '/' + new_file
        copy_to_newfile(old_file, new_file_path)
    return None


def copy_to_newfile(original_file:str, new_file:str) -> None:
    '''
    Copies the content of `original_file` to `new_file`.
    Used to create a new file from a template.
    '''
    original_file_path = get_file(original_file)
    with open(original_file_path, 'r') as f:
        template_content = f.readlines()
    with open(new_file, 'w') as new_file:
        new_file.writelines(template_content)
    return None


def template_to_newfile(template:str, new_file:str, comment:str) -> None:
    '''
    Same as `copy_as_newfile`, but adds a `comment`
    at the beginning of the new file.
    '''
    copy_to_newfile(template, new_file)
    with open(new_file, 'r') as file:
        lines = file.readlines()
    lines.insert(0, comment + '\n')
    with open(new_file, 'w') as file:
        file.writelines(lines)
    return None


def replace_str_on_keyword(text:str, keyword:str, file:str, only_first=False) -> None:
    '''
    Replaces the `keyword` string with the `text` string in the given `filename`.
    If `only_first=True`, it will only work
    at the first instance of the keyword, ignoring the rest.
    ```
    line... keyword ...line -> line... text ...line
    ```
    '''
    is_replacing = True
    file_path = get_file(file)
    with open(file_path, 'r') as f:
        lines = f.readlines()
    with open(file_path, 'w') as f:
        for line in lines:
            if keyword in line and is_replacing:
                line = line.replace(keyword, text)
                if only_first:
                    is_replacing = False
            f.write(line)
    return None


def replace_line_with_keyword(text:str, keyword:str, file:str, only_first=False) -> None:
    '''
    Replaces the full line containing the `keyword` string
    with the `text` string in the given `file`.
    If `only_first=True`, it will only work
    at the first instance of the keyword, ignoring the rest.
    ```
    line1
    keyword line2 -> text
    line3
    ```
    '''
    is_replacing = True
    file_path = get_file(file)
    with open(file_path, 'r') as f:
        lines = f.readlines()
    with open(file_path, 'w') as f:
        for line in lines:
            if keyword in line and is_replacing:
                line = text + '\n'
                if only_first:
                    is_replacing = False
            f.write(line)
    return None


def insert_text_under_keyword(text:str, keyword:str, file:str, only_first=False) -> None:
    '''
    Inserts the given `text` string under the first occurrence
    of the `keyword` in the given `file`.
    The keyword can be at any position within the line.
    If `only_first=True`, it will only work
    at the first instance of the keyword, ignoring the rest.
    ```
    line1
    keyword line2
    text
    line3
    ```
    '''
    file_path = get_file(file)
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


def replace_text_under_keyword(text:str, keyword:str, file:str) -> None:
    '''
    Replaces the lines under the first occurrence of the `keyword`
    in the given `filename` with the given `text` string.
    ```
    line1
    keyword line2
    text
    line4
    ```
    '''
    file_path = get_file(file)
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


def delete_text_under_keyword(keyword:str, file:str) -> None:
    '''
    Deletes the lines under the first occurrence of the `keyword` in the given `file`.
    ```
    lines...
    keyword
    (end of file)
    ```
    '''
    file_path = get_file(file)
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


def replace_text_between_keywords(text:str, key1:str, key2:str, file:str) -> None:
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
    delete_text_between_keywords(key1, key2, file)
    insert_text_under_keyword(text, key1, file)
    return None


def delete_text_between_keywords(key1:str, key2:str, file:str) -> None:
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
    file_path = get_file(file)
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


def correct_file_with_dict(file:str, fixing_dict:dict) -> None:
    '''
    Corrects the given `file` using the `fixing_dict` dictionary.
    '''
    file_path = get_file(file)
    found_key = False
    with open(file_path, 'r') as f:
        lines = f.readlines()
    for line in lines:
        if any(key in line for key in fixing_dict.keys()):
            found_key = True
            break
    if found_key:
        print("Correcting " + file_path + " ...")
        with open(file_path, 'w') as f:
            for line in lines:
                for key, value in fixing_dict.items():
                    line = line.replace(key, value)
                f.write(line)
    return None

