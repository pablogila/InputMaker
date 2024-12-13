'''
This script is used to update Thoth documentation automatically.
Requires pdoc, install it with `pip install pdoc`.
It also requires Thoth itself; installation instructions can be found in the README.md file.
Run this script as `python3 pdoc.py`.
'''

import thoth as th

version = th.text.find('version=', './thoth/__init__.py', -1)[0]
print(version)
version = th.extract.string(version, 'version', None, True)
print(f'Updating README to {version}...')
th.text.replace_line(f'# Thoth {version}', '# Thoth v','./README.md', 1)
print('Updating docs with Pdoc...')
th.call.shell(f"pdoc ./thoth/ -o ./docs --mermaid --math --footer-text='Thoth {version} documentation'")

