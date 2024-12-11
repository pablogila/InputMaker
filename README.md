# Thoth v4.0.0

Welcome to the '**T**ext **H**andling & **O**ptimization **T**oolkit **H**elper'; or just **Thoth**, as the Egyptian god of writing, wisdom and magic.  

This Python3 package allows you to create, edit and analyse all kind of text files, with a special focus to ab-initio calculations. Formally known as InputMaker.  

Just as the Egyptian god, Thoth is *married* with [Maat](https://github.com/pablogila/Maat), another super useful python package to analyze data from your experiments.  


## Installation

Thoth is installed as a regular Python package.
As always, it is recommended to install it in a virtual environment:  
```bash
python3 -m venv .venv
source .venv/bin/activate
```

Then, enter the downloaded `/Thoth/` directory, and install the package with pip:  
```bash
pip install .
```


## Documentation

Documentation is available locally on the `docs/inputmaker.html` folder.
An [online documentation](https://pablogila.github.io/InputMaker/) is also available.

This package contains the following submodules:
- [file](https://pablogila.github.io/Thoth/thoth/file.html). Manipulate files.
- [text](https://pablogila.github.io/Thoth/thoth/text.html). Read and manipulate text.
- [extract](https://pablogila.github.io/Thoth/thoth/extract.html). Extract data from raw text strings.
- [call](https://pablogila.github.io/Thoth/thoth/call.html). Run bash scripts and related (Linux)

The documentation can be compiled automatically using [pdoc](https://pdoc.dev/), by running:
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

