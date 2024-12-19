'''
This script is used to update Thoth documentation automatically.
Requires pdoc, install it with `pip install pdoc`.
It also requires Thoth itself; installation instructions can be found in the README.md file.
Run this script as `python3 pdoc.py`.
'''

import thoth as th

readme = './README.md'
temp_readme = './_README_temp.md'
version_path = './thoth/common.py'

fix_dict ={
    '[file](https://pablogila.github.io/Thoth/thoth/file.html)'         : '`thoth.file`',
    '[text](https://pablogila.github.io/Thoth/thoth/text.html)'         : '`thoth.text`',
    '[extract](https://pablogila.github.io/Thoth/thoth/extract.html)'   : '`thoth.extract`',
    '[alias](https://pablogila.github.io/Thoth/thoth/alias.html)'       : '`thoth.alias`',
    '[call](https://pablogila.github.io/Thoth/thoth/call.html)'         : '`thoth.call`',
    '[qe](https://pablogila.github.io/Thoth/thoth/call.html)'           : '`thoth.qe`',
    '[common](https://pablogila.github.io/Thoth/thoth/common.html)'     : '`thoth.common`',
    '[phonopy](https://pablogila.github.io/Thoth/thoth/phonopy.html)'   : '`thoth.phonopy`',
} 

version = th.text.find(r"version =", version_path, -1)[0]
version = th.extract.string(version, 'version', None, True)

print(f'Updating README to {version}...')
th.text.replace_line(f'# Thoth {version}', '# Thoth v', readme, 1)

print('Updating docs with Pdoc...')
th.file.from_template(readme, temp_readme, None, fix_dict)
th.call.shell(f"pdoc ./thoth/ -o ./docs --mermaid --math --footer-text='Thoth {version} documentation'")
th.file.remove(temp_readme)
print('Done!')

