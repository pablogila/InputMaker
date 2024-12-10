# InputMaker v3.0.1
This Python3 package allows you to make all kind of text files from a template file, thanks to a rich set of built-in functions.


## Installation

As always, it is recommended to install this package it in a virtual environment:  
```bash
python3 -m venv .venv
source .venv/bin/activate
```

Then, install the package with pip:  
```bash
pip install .
```

After installation, you can run InputMaker as a regular python package.
Most common tools are available to be called directly.
For example, to rename files with a specific extension in all subfolders:  
```python
>>> import inputmaker as im
>>> im.rename_files_on_subfolders('.psf_','.psf')
```

## Documentation

Documentation is available locally on the `docs/inputmaker.html` folder.
An [online documentation](https://pablogila.github.io/InputMaker/) is also available.

This package contains the following submodules:
- `InputMaker.file`. Manipulate files.
- `InputMaker.text`. Read and manipulate text.
- `InputMaker.extract`. Extract data from raw text strings.
- `InputMaker.call`. Run bash scripts and related (Linux)

