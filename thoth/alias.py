'''
# Description
Common dictionaries to normalise user inputs.

# Index
- `file`
- `boolean`

---
'''

file = {
    'file' : ['file', 'files', 'File', 'Files', 'FILE', 'FILES', 'f', 'F'],
    'dir'  : ['dir', 'Dir', 'DIR', 'directory', 'Directory', 'DIRECTORY', 'd', 'D', 'folder', 'Folder', 'FOLDER'],
    'Error' : ['Error', 'error', 'ERROR', 'Errors', 'errors', 'ERRORS'],
    }
'''
Strings related to files, to normalise user inputs.
'''

boolean= {
    True  : ['yes', 'YES', 'Yes', 'Y', 'y', 'T', 'True', 'TRUE', 't', 'true', True, 'Si', 'SI', 'si', 'S', 's'],
    False : ['no', 'NO', 'No', 'N', 'n', 'F', 'False', 'FALSE', 'f', 'false', False],
}
'''
Strings with booleans such as 'yes' / 'no', to correct user inputs.
'''

