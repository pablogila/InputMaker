# MakeCP2K  
Make CP2K inputs from a predefined input template file.  


## Dependencies  
- Python 3.X  
- ASE package. To install it, run:  
  `pip install ase`  


## File structure  

Download `input-maker.py` and place it near the CP2K input template file. There should be subfolders with the structural files to create the inputs. The file structure should look like this:  

```
root_folder
│
├── input-maker.py
├── CP2K_custom_template.inp
│
├── job_folder_1
│   ├── structural_file_1.pdb
│   └── ...
├── job_folder_2
│   ├── structural_file_2.pdb
│   └── ...
└── ...
```


## Template file  

The template must be specified in the `template` variable of `input-maker.py`. It should contain a keyword just before the ABC rows of the `&CELL` section, which will be replace by the updated cells. This keyword should be specified on the `template_cell_keyword` variable; by default, it is set to `'!REPLACE_CELL_HERE'`. The naming of the final input files is specified by the `final_file` variable. Finally, the format of the structural files used to extract the cell is specified on the `cell_format` variable, which by default is set to `'.pdb'`.  

An example of a cell section of a template file:  
```CP2K
&SUBSYS
    !!!!!!!!!! Cell section, must change depending on the size of the supercell !!!!!!!!!!
    &CELL
        A 35.767392000000008       0.000000000000000      0.000000000000000
        B 0.000000000000000      37.990278000000004       0.000000000000000
        C 0.000000000000000       0.000000000000000      33.906040000000004
        PERIODIC XYZ
        MULTIPLE_UNIT_CELL 1 1 1
    &END CELL
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
```

Currently, only the A, B and C rows are modified. Please make sure that the rest of the input template is correct.  


## Running input-maker.py  

Run the script with python (Windows), or python3 (Linux):  
```bash
python3 input-maker.py
```


## Optional: Reusing old inputs  

You can also reuse old `*.inp` files, by changing the extension to something else still containing the 'int' string, e.g., '.inp_'. You should specify that in the `cell_format`. It will then copy to the template just the ABC rows from the &CELL section, after the keyword.  


## Optional: Creating and sbatch'ing slurm files with SlurmGod  

MakeCP2K was designed to be used with [SlurmGod](https://github.com/pablogila/SlurmGod), a set of shell scripts to automatize the creation and sbatch'ing of slurm files.  

