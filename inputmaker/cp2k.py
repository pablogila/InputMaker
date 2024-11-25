'''
# Description
This submodule handles the creation of CP2K input files.
Still under heavy development.

# Index
- `cp2k()`
- `get_cell()`
- `get_cell_from_inp()`
- `get_cell_from_ase()`
- `get_coords()`

---
'''


from .tools import *
from .common import *
from ase.io import read


def cp2k():
    '''
    Create CP2K input files from a template.
    This function is still under heavy development.
    '''
    # Template files, must be in the same folder as this script:
    inp_template_extension = '.inp.template'
    slurm_template_extension = '.sh.template'
    # Keywords on the inp template file:
    key_cell = '!<keyword-cell>'
    key_coordinates = '!<keyword-coordinates>'
    key_topology_init = '!<keyword-topology-init>'
    key_topology_run = '!<keyword-topology-run>'
    key_topology_end = '!<keyword-topology-end>'
    key_pdb_filename = '!<keyword-pdb-filename>' # '        COORD_FILE_NAME ./dumped.pdb'
    key_psf_filename = '!<keyword-psf-filename>' # '        CONN_FILE_NAME ./dumped.psf'
    key_steps = '!<keyword-steps>'
    # Keywords on the slurm template file:
    key_jobname = '<keyword-JOBNAME>'
    key_filename = '<keyword-FILENAME>'
    ###########################################################################
    # Extension for an old input to be reused:
    old_inp_extension = '.inp.old'
    # Structural file extensions, ordered by priority:
    structure_extensions = [old_inp_extension, '.cif', '.cell', '.pdb']
    # If there are more than one structural file per folder, these ones will be preferred:
    preferred_structure_file = 'dumped.pdb'
    preferred_psf_file = 'dumped.psf'
    ###########################################################################
    # The psf file may have to be fixed for some weird reason...
    # https://dx.doi.org/10.1088/1361-648X/29/4/043001 (mattoni2016)
    # https://doi.org/10.1021/acs.jpcc.5b04283 (mattoni2015)
    fixing_psf = {
        'H       H     -99.000000' : 'H       H       0.023000',
        'C       C     -99.000000' : 'C       C       0.771000',
        'N       N     -99.000000' : 'N       N      -1.100000',
        'Pb      Pb    -99.000000' : 'Pb      Pb      2.030000',
        'I       I     -99.000000' : 'I       I      -1.130000',
        'D       D     -99.000000' : 'D       D       0.540000',
    }
    ###########################################################################

    # Initialize the warning flags:
    only_one_slurm_per_folder = True
    is_first_run_needed = False

    print(welcome('CP2K'))

    path = os.getcwd()
    inp_template = get_files_from_folder(path, inp_template_extension)
    inp_template = get_file(inp_template[0])
    slurm_template = get_files_from_folder(path, slurm_template_extension)
    slurm_template = get_file(slurm_template[0])

    new_inp_name = inp_template.replace(inp_template_extension, '.inp')

    if slurm_template is None: # Warning will be printed at the end
        new_slurm_name = None
    else:
        new_slurm_name = slurm_template.replace(slurm_template_extension, '.sh')

    for folder in os.listdir('.'):
        if os.path.isdir(folder):

            structure_name = get_file_from_folder(folder, structure_extensions, preferred_structure_file)
            if structure_name is None:
                continue
            else:
                structure_file = os.path.join(folder, structure_name)

            new_inp_path = os.path.join(folder, new_inp_name)

            psf_file = get_file_from_folder(folder, '.psf', preferred_psf_file)
            pdb_file = get_file_from_folder(folder, '.pdb', preferred_structure_file)

            cell = get_cell(structure_file)
            if cell is None:
                continue

            template_to_file(inp_template, new_inp_path, "! This file was created from " + inp_template + " with " + name() + " " + version())

            replace_lines_under_keyword(cell, key_cell, new_inp_path)

            if not psf_file: # 1st run
                is_first_run_needed = True # Raise a warning flag
                positions = get_coords(structure_file)
                if positions is None:
                    continue
                template_to_file(new_inp_path, new_inp_path, "! WARNING: Perform a first run of CP2K to create the *.psf file, then run again " + name() + " and CP2K.")
                delete_lines_between_keywords(key_topology_run, key_topology_end, new_inp_path)
                insert_lines_under_keyword(positions, key_coordinates, new_inp_path)
                replace_lines_under_keyword(['    STEPS 1'], key_steps, new_inp_path)

                print("  Created " + new_inp_path + " (without a *.psf file!)")
                print("  IMPORTANT: Run CP2K to create the *.psf file, then run again " + name() + " and CP2K.")

            else: # 2nd run
                delete_lines_between_keywords(key_topology_init, key_topology_run, new_inp_path)
                replace_lines_under_keyword(['        COORD_FILE_NAME ./' + pdb_file], key_pdb_filename, new_inp_path)
                replace_lines_under_keyword(['        CONN_FILE_NAME ./' + psf_file], key_psf_filename, new_inp_path)

                correct_file_with_dict(os.path.join(folder, psf_file), fixing_psf) # Fix the psf file if needed

                print("  Created " + new_inp_path)

            if slurm_template: # Create slurm file
                new_slurm_path = os.path.join(folder, new_slurm_name)
                copy_as_newfile(slurm_template, new_slurm_path)
                replace_str_on_keyword(folder, key_jobname, new_slurm_path)
                replace_str_on_keyword(new_inp_name.replace('.inp', ''), key_filename, new_slurm_path)
                if not psf_file:
                    replace_full_line_with_keyword('#SBATCH --time=00:02:00', '#SBATCH --time=', new_slurm_path)
                print("  Created " + new_slurm_path)
            
            if count_files(folder, '.sh') != 1:
                only_one_slurm_per_folder = False # Raise a warning flag

            print("")
    
    print("  Done!")
    if is_first_run_needed:
        print("  WARNING: Running without a *.psf file is an experimental feature, it may not work...")
    if only_one_slurm_per_folder and slurm_template:
        print("  Run all inputs at once with 'source sbatch_all.sh'\n")
    elif not slurm_template:
        print("  WARNING: No *" + slurm_template_extension + " slurm template found in path, you will have to create slurms manually!\n")
    else:
        print("  WARNING: More than one *.sh file per folder. You should sbatch' them one by one.\n")


def get_cell(structure_file):
    '''
    Returns a string with the proper cell parameters from `structure_file`,
    formatted to be included in a CP2K input file.
    '''
    if '.inp' in structure_file:
        method = 'get_cell_from_inp() from InputMaker' + tools.version
        rows = get_cell_from_inp(structure_file)
    else:
        method = 'get_cell_from_ase() from InputMaker ' + tools.version
        rows = get_cell_from_ase(structure_file)
    if rows == None or len(rows) != 3:
        raise ValueError("ERROR: Didn't find the cell parameters in " + structure_file)

    cell = [None, None, None, None]
    cell[0] = "        A   " + rows[0]
    cell[1] = "        B   " + rows[1]
    cell[2] = "        C   " + rows[2]
    cell[3] = "        ! These cell parameters were obtained from " + structure_file + " with " + method
    return cell


def get_cell_from_inp(inp_file):
    '''
    Returns the cell parameters from a previous CP2K `inp_file` input file.
    '''
    with open(inp_file, 'r') as f:
        inp_content = f.readlines()
    cell_rows = [None, None, None]
    for i, line in enumerate(inp_content):
        if line.strip() == '&CELL':
            for j in range(3):
                row = inp_content[i+j+1].strip()
                if row.startswith(('A ', 'B ', 'C ')):
                    cell_rows[j] = row[2:]
            return tuple(cell_rows)
    return None


def get_cell_from_ase(structure_file):
    '''
    Returns the cell parameters from a given `structure_file` using ASE,
    '''
    try:
        structure = read(structure_file)
        cell = structure.cell[:]
        transposed_cell = zip(*cell)
        cell_rows = ['     '.join(f"{num:.15f}" for num in row) for row in transposed_cell]
        return tuple(cell_rows)
    except:
        return None


def get_coords(structure_file):
    '''
    Returns a list of strings with the atomic positions from `structure_file`,
    ready to be used in a CP2K input file.
    '''
    try:
        structure = read(structure_file)
        symbols = structure.get_chemical_symbols()
        coords = structure.get_positions()
        coords_with_symbols = ['{} {:0.6f} {:0.6f} {:0.6f}'.format(symbol, *coord) for symbol, coord in zip(symbols, coords)]
        coords_with_symbols.append('!These positions were obtained from ' + structure_file + ' with the method get_coords() of InputMaker ' + version())
        return coords_with_symbols
    except:
        raise ValueError("ERROR: Didn't find the atom positions in " + structure_file)

