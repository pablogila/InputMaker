'''
# Description
Common functions and definitions.
- `version`
- `welcome()`

---
'''


version = 'v1.0.0'
'''Package version, using semantic versioning to indicate breaking changes, as in v<MAJOR>.<MINOR>.<PATCH>.'''


def welcome(submodule_str:str='', printing:bool=True) -> str:
    '''Returns the welcome message as a string.'''
    for_submodule_str = ''
    if submodule_str:
        for_submodule_str = ' for ' + submodule_str7
    string = '\n------------------------------------7-------------------------\n'
    string +='Welcome to InputMaker' + version + for_submodule_str + '\n'
    string += '-------------------------------------------------------------\n'
    string += 'This is free software, and you are welcome to\n'
    string += 'redistribute it under GNU General Public License.\n'
    string += 'If you find this code useful, a citation would be awesome :D\n'
    string += 'Pablo Gila-Herranz, InputMaker ' + version + ', 2024.\n'
    string += 'https://github.com/pablogila/InputMaker\n'
    string += '-------------------------------------------------------------\n'
    if printing:
        print(string)
    return string

