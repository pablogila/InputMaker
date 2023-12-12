# Input Maker   
Make all kind of inputs from a template file, thanks to a rich set of built-in functions.  
Currently supports CP2K inputs, but can be easily extended to other packages.  


### Dependencies  
- Python 3.X  
- ASE package. To install it, run `pip install ase`.  


## Running inputmaker.py  

`inputmaker.py` can be easily imported and run from the command line or from another script, to use its built-in functions. But you can also run the script with python (Windows), or python3 (Linux), with an optional flag to create a specific kind of input. Notice that the file structure should have been previously configured, as described in the section [File structure](#file-structure). To create CP2K inputs:  

```bash
python3 inputmaker.py -cp2k
```

To use the built-in functions from the command line, for example, to rename files with a specific extension in all subfolders:  

```python
>>> import inputmaker as im
>>> im.rename_files_on_subfolders('.psf_','.psf')
```

Currently, only CP2K inputs are supported. However, the script can be easily expanded to create other types of inputs.


## Built-in functions  

The power of `inputmaker.py` resides on its built-in functions, related to file manipulation and text processing. These functions make it really easy to create and modify all kind of templates.  
A function named `cp2k()` is already predefined to create CP2K inputs. However, the script can be expanded with custom functions to create other types of inputs, thanks to its modular structure. A brief description of the built-in function is given below:  

- `get_files(folder, extensions)`. Retrieves all files from a given folder that match the provided extensions. It returns a list of these files.  

- `get_file(folder, extensions, preference=None)`. Retrieves a specific file from a given folder based on the provided extensions and preference. If multiple files match the criteria, it returns the file that contains the preference in its name. If no preference is provided or no file matches the preference, but there are multiple files with the given extensions, it prints an error message and returns None. If only one file matches the extensions, it returns that file. Depends on get_files(). Usage: get_file('/path/to/folder', ['.txt', '.doc'], 'preferred_file.txt').  

- `count_files(folder, extension)`: Counts the number of files in a given folder that match the provided extension. Depends on get_files(). Usage: count_files('/path/to/folder', '.txt').  

- `copy_as_newfile(template, new_file)`: Copies the content of a template file to a new file.  

- `template_to_newfile(template, new_file, comment)`: Copies the content of a template file to a new file and inserts a comment at the beginning of the new file. Depends on copy_as_newfile().  

- `delete_lines_between_keywords(key1, key2, filepath)`: Deletes lines between two keywords in a file. Usage: delete_lines_between_keywords('#key_start', '#key_end', 'file.txt').  

- `add_lines_under_keyword(lines, keyword, filename)`: Adds lines under a specific keyword in a file. Usage: add_lines_under_keyword(['line1', 'line2'], 'keyword', 'file.txt').  

- `replace_lines_under_keyword(lines, keyword, filename)`: Replaces lines under a specific keyword in a file. Usage: replace_lines_under_keyword(['new line1', 'new line2'], 'keyword', 'file.txt').  

- `replace_full_line_with_keyword(new_text, keyword, filename)`: Replaces a full line containing a specific keyword in a file with new text. Usage: replace_full_line_with_keyword('new text', 'keyword', 'file.txt').  

- `replace_str_on_keyword(new_text, keyword, filename)`: Replaces a specific keyword in a file with new text. Usage: replace_str_on_keyword('new text', 'keyword', 'file.txt').  

- `correct_file_with_dict(filename, fixing_psf)`: Corrects a file by replacing specific keywords with corresponding values from a dictionary. Usage: correct_file_with_dict('file.txt', {'old1': 'new1', 'old2': 'new2'}).  

- `get_cell(structure_file, alternate_extension='.inp.old')`: Retrieves cell parameters from a structure file. Depends on get_cell_from_inp() and get_cell_from_ase(), and returns the cell parameters in the CP2K format.

- `get_cell_from_ase(structure_file_path)`: Retrieves cell parameters from an ase file.  

- `get_cell_from_inp(inp_file_path)`: Retrieves cell parameters from an old inp file.  

- `get_coords(structure_file_path)`: Retrieves atomic positions from a structure file, using ASE.  

- `rename_files_on_subfolders(old_extension, new_extension)`: Renames files with a specific old extension to a new extension in all subfolders. It is usefull to import the script and use this function on the command line, to prepare the inputs. Usage: rename_files_on_subfolders('.inp', '.inp.old')


## CP2K inputs

The template for CP2K inputs should contain several keywords, where the text will be replaced. For instance, you need a keyword just before the ABC rows of the `&CELL` section, which will be replaced by the updated cells. This keyword should be specified on the `key_cell` variable of the `cp2k()` function.  
An example of a cell section of a template file:  

```CP2K
&SUBSYS
    &CELL
!<keyword-cell>
        A 1.000000000000000       0.000000000000000       0.000000000000000
        B 0.000000000000000       1.000000000000000       0.000000000000000
        C 0.000000000000000       0.000000000000000       1.000000000000000
        ! Line reserved for debugging, immediatly under cell parameters. DO NOT WRITE HERE.

        !!! Make sure that the following parameters are correct! input-maker does not check them.
        PERIODIC XYZ
        MULTIPLE_UNIT_CELL 1 1 1
    &END CELL
```

The keys are defined on the `cp2k()` function, as follows:  
```python
# Template files, must be in the same folder as this script:
inp_template_extension = '.inp.template' # CP2K input template
slurm_template_extension = '.sh.template' # Slurm file template
# Keywords on the inp template file:
key_cell = '!<keyword-cell>' # Right above the ABC rows of the &CELL section
key_coordinates = '!<keyword-coordinates>' # On the &COORD section 
key_topology_init = '!<keyword-topology-init>' 
key_topology_run = '!<keyword-topology-run>'
key_topology_end = '!<keyword-topology-end>'
key_pdb_filename = '!<keyword-pdb-filename>' # '        COORD_FILE_NAME ./dumped.pdb'
key_psf_filename = '!<keyword-psf-filename>' # '        CONN_FILE_NAME ./dumped.psf'
key_steps = '!<keyword-steps>' # Before the number of steps
# Keywords on the slurm template file:
key_jobname = '<keyword-JOBNAME>'
key_filename = '<keyword-FILENAME>'
```

Notice that for CP2K inputs, a PDB and a PSF file are required. The PDB file is used to get the coordinates, and the PSF file is used to get the topology. Both files are detected automatically; however, in case the PSF file is not found, the script can create an initial input file so that CP2K can quickly generate it. After that, run again inputmaker and CP2K for a second time, now with the PSF file available. The keywords for the topology section are then used to place the coordinates and the topology in the correct places, as follows:  

```CP2K
!!!  ONLY RUN 1st TIME (without PSF file)  !!!
!<keyword-topology-init>
    &COORD
        SCALED .TRUE.
!<keyword-coordinates>
    &END COORD   
    &TOPOLOGY
        &generate
            bondparm covalent 
            BONDLENGTH_MAX 3.5
            bondparm_factor 1.0
            create_molecules .true.
        &end generate
        &CENTER_COORDINATES
        &END CENTER_COORDINATES
        CONNECTIVITY GENERATE
        &DUMP_PDB
        &END
        &DUMP_PSF
        &END
!!!  RUN 2nd time, ONCE YOU HAVE PDB & PSF FILES  !!!
!<keyword-topology-run>
    &TOPOLOGY
        COORD_FILE_FORMAT PDB
!<keyword-pdb-filename>
        COORD_FILE_NAME ./dumped.pdb
        CONNECTIVITY psf
!<keyword-psf-filename>
        CONN_FILE_NAME ./dumped.psf
!<keyword-topology-end>
    &END TOPOLOGY
```


### File structure  

Download `inputmaker.py` and place it near the input template file, in this case, a CP2K input. There should be subfolders with the structural files to create the inputs. The file structure should look like this:  

```
root_folder
│
├── inputmaker.py
├── sbatch_all.sh
├── custom_input.inp.template
├── custom_slurm.sh.template
│
├── job_folder_1
│   ├── structural_file_1.pdb
│   ├── structural_file_1.psf
│   └── ...
├── job_folder_2
│   ├── structural_file_2.pdb
│   └── ...
└── ...
```


### Optional: Reusing old CP2K inputs  

You can also reuse old `*.inp` files, by changing the extension to `.inp.old`. It will then copy to the template just the ABC rows from the &CELL section, after the keyword.  


## Sbatch'ing slurm files  

If there is only one `*.sh` slurm file per folder, you can sbatch' all inputs with the command:  

```bash
source sbatch_all.sh
```

