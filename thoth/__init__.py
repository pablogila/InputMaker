'''
.. include:: ../README.md
    :end-before: Documentation

## Documentation

Documentation is available locally on the `docs/inputmaker.html` folder.
An [online documentation](https://pablogila.github.io/InputMaker/) is also available.

This package contains the following submodules:
- `thoth.file`. Manipulate files
- `thoth.text`. Read and manipulate text
- `thoth.extract`. Extract data from raw text strings
- `thoth.call`. Run bash scripts and related

Additionally, some specific modules for use in tandem with ab-initio codes are included:
- `thoth.qe`. Specific module for Quantum ESPRESSO.

The documentation can be compiled automatically using [pdoc](https://pdoc.dev/) and Thoth itself, by running:
```shell
source pdoc.sh
```


## License

> TL;DR: Do what you want with this, as long as you share the source code of your modifications, also under GNU AGPLv3.  

Copyright (C) 2024  Pablo Gila-Herranz

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the attached GNU Affero General Public License for more details.
'''


from . import alias
from . import file
from . import call
from . import text
from . import extract
from . import qe


version='v4.3.1'
'''
Package version, using semantic versioning to indicate breaking changes,
as in v<MAJOR>.<MINOR>.<PATCH>.
'''

