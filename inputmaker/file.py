'''
# Description
Functions to manipulate files.

# Index
- `get()`
- `copy()`
- `move()`
- `remove()`
- `rename()`
- `rename_on_subfolders()`
- `copy_to_subfolders()`
- `from_template()`

---
'''


import os
import shutil


def get(file:str, filters=None, only_filenames:bool=False):
    '''
    Check if the given `file` exists in the currrent working directory
    or in the full path, and returns its full path as a **string**.\n
    If the provided string is a directory, returns a **list** of files inside it.
    In this case, the listed files are filtered by the given `filters` if provided.
    By default, the full file paths will be included in the list.
    To return a list with only the file names, set `only_filenames=True`. 
    '''
    if os.path.isfile(file):
        return os.path.abspath(file)
    elif os.path.isdir(file):
        file = os.path.abspath(file)
        files = os.listdir(file)
    else:
        raise FileNotFoundError('Nothing found at ' + file)
    # Apply filters or not
    if filters is not None:
        target_files = []
        if not isinstance(filters, list):
            filters = [filters]
        for filter_i in filters:
            for f in files:
                if filter_i in f:
                    target_files.append(f)
        files = target_files
    # Return file names or file paths
    if not only_filenames:
        filepaths = []
        for f in files:
            filepaths.append(os.path.join(file, f))
        files = filepaths
    return files


def copy(original_file:str, new_file:str) -> None:
    '''
    Copies the content of `original_file` to `new_file`.
    '''
    original_file_path = get(original_file)
    file = shutil.copy(original_file_path, new_file)
    return None


def move(original_file:str, new_file:str) -> None:
    '''
    Moves `original_file` to `new_file`.
    '''
    original_file_path = get(original_file)
    file = shutil.move(original_file_path, new_file)
    return None


def remove(file:str) -> None:
    '''
    Removes the given `file`.
    '''
    file_path = get(file)
    shutil.rmtree(file_path)
    return None


def rename(old_string:str, new_string:str, folder=None) -> None:
    '''
    Batch renames files in the given folder, replacing `old_string` by `new_string`.
    If no `folder` is provided, the current working directory is used.
    '''
    if folder is None:
        files = os.listdir('.')
    elif os.path.isdir(folder):
        files = os.listdir(folder)
    elif os.path.isdir(os.path.join(os.getcwd(), folder)):
        files = os.listdir(os.path.join(os.getcwd(), folder))
    else:
        raise FileNotFoundError('Missing folder at ' + folder + ' or in the CWD ' + os.getcwd())
    for f in files:
        if old_string in f:
            os.rename(f, f.replace(old_string, new_string))
    return None


def rename_on_subfolders(old_string:str, new_string:str, folder=None) -> None:
    '''
    Renames the files inside the subfolders in the given `folder`,
    from an `old_string` to the `new_string`.
    If no `folder` is provided, the current working directory is used.
    '''
    if folder is None:
        things = os.listdir('.')
    elif os.path.isdir(folder):
        things = os.listdir(folder)
    elif os.path.isdir(os.path.join(os.getcwd(), folder)):
        things = os.listdir(os.path.join(os.getcwd(), folder))
    else:
        raise FileNotFoundError('Missing folder at ' + folder + ' or in the CWD ' + os.getcwd())
    for d in things:
        if os.path.isdir(d):
            for f in os.listdir(d):
                if old_string in f:
                    old_file = os.path.join(d, f)
                    new_file = os.path.join(d, f.replace(old_string, new_string))
                    os.rename(old_file, new_file)
    return None


def copy_to_subfolders(folder=None, extension:str=None, strings_to_delete:list=[]) -> None:
    '''
    Copies the files from the `folder` with the given `extension` to individual subfolders.
    The subfolders are named as the original files,
    removing the strings from the `strings_to_delete` list.
    If no `folder` is provided, it runs in the current working directory.
    '''
    if folder is None:
        folder = os.getcwd()
    old_files = get(folder, extension)
    if old_files is None:
        raise ValueError('No ' + extension + ' files found in path!')
    for old_file in old_files:
        new_file = old_file
        for string in strings_to_delete:
            new_file = new_file.replace(string, '')
        path = new_file.replace(extension, '')
        os.makedirs(path)
        new_file_path = path + '/' + new_file
        copy(old_file, new_file_path)
    return None


def from_template(template:str, new_file:str, comment:str) -> None:
    '''
    Same as `copy_file`, but adds a `comment`
    at the beginning of the new file.
    '''
    copy(template, new_file)
    with open(new_file, 'r') as file:
        lines = file.readlines()
    lines.insert(0, comment + '\n')
    with open(new_file, 'w') as file:
        file.writelines(lines)
    return None

