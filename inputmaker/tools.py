'''
# Description
Common functions to read, write and extract information from different files.

# Index
- `welcome()`
- `get_file_with_extension()`
- `get_files_with_extension()`
- `count_files_with_extension()`
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


version = 'v0.2.0'
'''Package version, using semantic versioning to indicate breaking changes, as in v<MAJOR>.<MINOR>.<PATCH>.'''


def welcome(submodule_str=''):
    '''Returns the welcome message.'''
    for_submodule_str = ''
    if submodule_str:
        for_submodule_str = ' for ' + submodule_str + ' inputs.'
    string = '\n-------------------------------------------------------------\n'
    string +='Welcome to InputMaker' + version + for_submodule_str + '\n'
    string += 'You should already have cif2cell installed on your system.\n'
    string += '-------------------------------------------------------------\n'
    string += 'This is free software, and you are welcome to\n'
    string += 'redistribute it under GNU General Public License.\n'
    string += 'If you find this code useful, a citation would be awesome :D\n'
    string += 'Pablo Gila-Herranz, InputMaker ' + version + ', 2024.\n'
    string += 'https://github.com/pablogila/InputMaker\n'
    string += '-------------------------------------------------------------\n'
    return string


def get_file_with_extension(folder, extensions, preference=None):
    '''
    Returns the file with one of the the specified `extensions`
    (string or list with strings) in the given `folder`.
    If there is more than one file with the extension,
    it returns the one containing the `preference` string.
    '''
    files = get_files(folder, extensions)
    if files is None:
        return None
    if len(files) > 1:
        for file in files:
            if preference in file:
                return file
        raise ValueError(folder + ' contains too many ' + extensions + ' files!')
        #print("  ERROR: " + folder + " contains too many " + extensions + " files, skipping...")
    return files[0]


def get_files_with_extension(folder, extensions):
    '''
    Returns a list with the files in a given `folder`
    with the the specified `extensions` (string or list with strings).
    '''
    files = os.listdir(folder)
    target_files = []
    if not isinstance(extensions, list):
        extensions = [extensions]
    for extension in extensions:
        for file in files:
            if file.endswith(extension):
                target_files.append(file)
        if target_files:
            return target_files
    return None


def count_files_with_extension(folder, extension):
    '''
    Returns the number of files with the specified `extension` (string or list of strings) in the given `folder`.
    '''
    files = get_files(folder, extension)
    if files is None:
        return 0
    return len(files)


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
        for i, coord in enumerate(lines):
            document.insert(index + 1 + i, "        " + coord + "\n")
        with open(file, 'w') as file:
            file.writelines(document)
    else:
        raise ValueError("Didn't find the '" + keyword + "' keyword in " + file)
        #print("  ERROR:  Didn't find the '" + keyword + "' keyword in " + file)


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
        #print("  ERROR: Didn't find the '" + keyword + "' keyword in " + filename)


def delete_lines_under_keyword(keyword:str, file:str):
    pass #TODO


def replace_lines_between_keywords(text:str, key1:str, key2:str, file:str)
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
        if not skip or key1 in line or key2 in line:
            keep.append(line)
    with open(file, 'w') as f:
        f.writelines(keep)


def correct_file_with_dict(file, fixing_dict):
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

