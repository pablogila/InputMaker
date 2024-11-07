'''
# Description
Common functions to manipulate input files with custom keywords.

# Index
- `get_file()`
- `get_files_from_folder()`
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


def get_file(file):
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


def get_files_from_folder(folder, extensions=None):
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


def rename_files(old_string:str, new_string:str):
    '''
    Renames files in the current working directory,
    replacing the `old_string` by the `new_string`.
    '''
    for file in os.listdir('.'):
        if old_string in file:
            os.rename(file, file.replace(old_string, new_string))


def rename_files_on_subfolders(old_extension:str, new_extension:str):
    '''
    Renames the files with the `old_extension` to the `new_extension`.
    Runs in the current working directory.
    '''
    for folder in os.listdir('.'):
        if os.path.isdir(folder):
            for file in os.listdir(folder):
                if file.endswith(old_extension):
                    old_file = os.path.join(folder, file)
                    new_file = os.path.join(folder, file.replace(old_extension, new_extension))
                    os.rename(old_file, new_file)


def copy_files_to_subfolders(extension, words_to_delete=[]):
    '''
    Copies the files with the given `extension` to individual subfolders.
    Runs in the current working directory.
    '''
    path = os.getcwd()
    old_files = get_files(path, extension)
    if old_files is None:
        raise ValueError('No ' + extension + ' files found in path!')
        #print("  WARNING: no " + extension + " files found in path, skipping...\n")
        return
    for old_file in old_files:
        new_file = old_file
        for word in words_to_delete:
            new_file = new_file.replace(word, '')
        folder = new_file.replace(extension, '')
        os.makedirs(folder)
        new_file_path = folder + '/' + new_file
        copy_as_newfile(old_file, new_file_path)


def copy_to_newfile(original_file, new_file):
    '''
    Copies the content of `original_file` to `new_file`.
    Used to create a new file from a template.
    '''
    with open(original_file, 'r') as f:
        template_content = f.readlines()
    with open(new_file, 'w') as new_file:
        new_file.writelines(template_content)
    return


def template_to_newfile(template, new_file, comment:str):
    '''
    Same as `copy_as_newfile`, but adds a `comment`
    at the beginning of the new file.
    '''
    copy_as_newfile(template, new_file)
    with open(new_file, 'r') as file:
        lines = file.readlines()
    lines.insert(0, comment + '\n')
    with open(new_file, 'w') as file:
        file.writelines(lines)


def replace_str_on_keyword(text:str, keyword:str, file:str):
    '''
    Replaces the `keyword` string with the `text` string in the given `filename`.
    '''
    with open(file, 'r') as file:
        lines = file.readlines()
    with open(file, 'w') as file:
        for line in lines:
            if keyword in line:
                line = line.replace(keyword, text)
            file.write(line)
    return


def replace_line_with_keyword(text:str, keyword:str, file:str):
    '''
    Replaces the full line containing the `keyword` string
    with the `text` string in the given `file`.
    '''
    with open(file, 'r') as file:
        lines = file.readlines()
    with open(file, 'w') as file:
        for line in lines:
            if keyword in line:
                line = text + '\n'
            file.write(line)
    return


def insert_lines_under_keyword(lines:str, keyword:str, file:str):
    '''
    Inserts the given `lines` string under the first occurrence
    of the `keyword` in the given `file`.
    '''
    with open(file, 'r') as file:
        document = file.readlines()
    index = next((i for i, line in enumerate(document) if line.strip().startswith(keyword)), None)
    if index is not None:
        for i, line in enumerate(lines):
            document.insert(index + 1 + i, line + "\n")
        with open(file, 'w') as file:
            file.writelines(document)
    else:
        raise ValueError("Didn't find the '" + keyword + "' keyword in " + file)
    return


def replace_lines_under_keyword(lines:str, keyword:str, file:str):
    '''
    Replaces the lines under the first occurrence of the `keyword`
    in the given `filename` with the given `lines` string.
    '''
    with open(file, 'r') as file:
        document = file.readlines()
    index = next((i for i, line in enumerate(document) if line.strip().startswith(keyword)), None)
    if index is not None:
        for i, row in enumerate(lines):
            if index + 1 + i < len(document):
                document[index + 1 + i] = row + "\n"
        with open(file, 'w') as file:
            file.writelines(document)
    else:
        raise ValueError("Didn't find the '" + keyword + "' keyword in " + file)
    return


def delete_lines_under_keyword(keyword:str, file:str):
    pass #TODO


def replace_lines_between_keywords(text:str, key1:str, key2:str, file:str):
    '''TO-CHECK'''
    delete_lines_between_keywords(key1, key2, file)
    insert_lines_under_keyword(text, key1, file)
    return


def delete_lines_between_keywords(key1:str, key2:str, file:str):
    '''Deletes the lines between two keywords in a given `file`.'''
    with open(file, 'r') as f:
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
    with open(file, 'w') as f:
        f.writelines(keep)
    return


def correct_file_with_dict(file, fixing_dict:dict):
    '''
    Corrects the given `file` using the `fixing_dict` dictionary.
    '''
    found_key = False
    with open(file, 'r') as file:
        lines = file.readlines()
    for line in lines:
        for key in fixing_dict.keys():
            if key in line:
                found_key = True
                break
        if found_key:
            print("Correcting " + file + "...")
            for key, value in fixing_dict.items():
                replace_str_on_keyword(value, key, filename)
            break
    return

