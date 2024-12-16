# Thoth v4.3.2

Welcome to **T**he **H**elpful & **O**ptimized **T**ext **H**elper; or just **Thoth**, as the Egyptian god of writing, wisdom and magic.  

This Python3 package allows you to create, edit and analyze all kinds of text files, with a special focus on ab-initio calculations. Formally known as InputMaker.  

Just as the Egyptian god, Thoth is *married* with [Maat](https://github.com/pablogila/Maat), another super useful python package to analyze data from your experiments. Although Maat is not required to run Thoth, it is super useful anyway, so check it out.  


## Installation

Thoth is installed as a regular Python package.
As always, it is recommended to install it in a virtual environment:  
```bash
python3 -m venv .venv
source .venv/bin/activate
```

Then, clone the repository from [GitHub](https://github.com/pablogila/Thoth/) or download it as a ZIP and run inside the `/Thoth/` directory:  
```bash
pip install .
```


## Documentation

Documentation is available locally on the `docs/thoth.html` folder.
An [online documentation](https://pablogila.github.io/InputMaker/) is also available.

This package contains the following submodules:
- [file](https://pablogila.github.io/Thoth/thoth/file.html). Manipulate files.
- [text](https://pablogila.github.io/Thoth/thoth/text.html). Read and manipulate text.
- [extract](https://pablogila.github.io/Thoth/thoth/extract.html). Extract data from raw text strings.
- [alias](https://pablogila.github.io/Thoth/thoth/alias.html). Common dictionaries to normalise user inputs.
- [call](https://pablogila.github.io/Thoth/thoth/call.html). Run bash scripts and related.

Additionally, some specific modules for use in tandem with ab-initio codes are included:
- [qe](https://pablogila.github.io/Thoth/thoth/call.html). Specific module for Quantum ESPRESSO.

The documentation can be compiled automatically using [pdoc](https://pdoc.dev/) and Thoth itself, by running:
```shell
python3 pdoc.py
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

