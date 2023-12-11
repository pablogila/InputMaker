import os
import glob
try:
    from ase.io import read
except:
    print("  ERROR:  ASE package not found, install it with 'pip install ase'")
    exit()


###########################################################################
## Create CP2K input files from a template, easy piecy.
###########################################################################
# Keywords inp:
key_cell = '!<keyword-cell>'
key_coordinates = '!<keyword-coordinates>'
key_topology_init = '!<keyword-topology-init>'
key_topology_run = '!<keyword-topology-run>'
key_topology_end = '!<keyword-topology-end>'
key_pdb_filename = '!<keyword-pdb-filename>' # '        COORD_FILE_NAME ./dumped.pdb'
key_psf_filename = '!<keyword-psf-filename>' # '        CONN_FILE_NAME ./dumped.psf'
key_steps = '!<keyword-steps>'
# Keywords slurm:
key_jobname = '<keyword-JOBNAME>'
key_filename = '<keyword-FILENAME>'
###########################################################################
old_inp_extension = '.inp.old'
structure_extensions = [old_inp_extension, '.cif', '.cell', '.pdb'] # Ordered by priority
preferred_structure_file = 'dumped.pdb'
###########################################################################
# The psf file needs to be fixed for some weird reason.
fixing_psf = {
    'H       H     -99.000000' : 'H       H       0.023000',
    'C       C     -99.000000' : 'C       C       0.771000',
    'N       N     -99.000000' : 'N       N      -1.100000',
    'Pb      Pb    -99.000000' : 'Pb      Pb      2.030000',
    'I       I     -99.000000' : 'I       I      -1.130000',
    'D       D     -99.000000' : 'D       D       0.540000',
}
###########################################################################


def version():
    return 'input-maker.2023.12.11.1500'


def cp2k():

    only_one_sh_per_folder = True

    welcome_cp2k()

    path = os.getcwd()

    inp_template = get_file(path, '.inp.template')
    slurm_template = get_file(path, '.sh.template')

    if inp_template is None:
        print("  ERROR:  No '*.inp.template' input found in path, exiting...")
        exit()
    new_inp_name = inp_template.replace('.template','')

    if slurm_template is None:
        print("  WARNING:  No '*.sh.template' slurm template found in path, you will have to run manually")
        new_slurm_name = None
    else:
        new_slurm_name = slurm_template.replace('.template','')

    for folder in os.listdir('.'):
        if os.path.isdir(folder):

            structure_name = get_file(folder, structure_extensions, preferred_structure_file)
            if structure_name is None:
                continue
            else:
                structure_file = os.path.join(folder, structure_name)

            new_inp_path = os.path.join(folder, new_inp_name)

            psf_file = get_file(folder, '.psf')
            pdb_file = get_file(folder, '.pdb', preferred_structure_file)

            cell = get_cell(structure_file)
            if cell is None:
                continue

            newfile_from_template(new_inp_path, inp_template)

            replace_lines_under_keyword(cell, key_cell, new_inp_path)

            if not psf_file: # 1st run
                positions = get_coords(structure_file)
                if positions is None:
                    continue
                delete_lines_between_keywords(key_topology_run, key_topology_end, new_inp_path)
                add_lines_under_keyword(positions, key_coordinates, new_inp_path)
                replace_lines_under_keyword(['    STEPS 1'], key_steps, new_inp_path)

                print("  FIRST RUN:  Run CP2K to create the *.psf file, then run input-maker and CP2K again")
                print("  Created " + new_inp_path)

            else: # 2nd run
                delete_lines_between_keywords(key_topology_init, key_topology_run, new_inp_path)
                replace_lines_under_keyword(['        COORD_FILE_NAME ./' + pdb_file], key_pdb_filename, new_inp_path)
                replace_lines_under_keyword(['        CONN_FILE_NAME ./' + psf_file], key_psf_filename, new_inp_path)

                correct_psf(psf_file, fixing_psf)

                print("  Created " + new_inp_path)

            if slurm_template:
                new_slurm_path = os.path.join(folder, new_slurm_name)
                copy_as_newfile(slurm_template, new_slurm_path)
                replace_str_on_keyword(folder, key_jobname, new_slurm_path)
                replace_str_on_keyword(new_inp_name.replace('.inp', ''), key_filename, new_slurm_path)
                if not psf_file:
                    replace_full_line_with_keyword('#SBATCH --time=00:02:00', '#SBATCH --time=', new_slurm_path)
                print("  Created " + new_slurm_path)
            
            if count_files(folder, '.sh') > 1:
                only_one_sh_per_folder = False

            print("")
    
    if only_one_sh_per_folder:
        print("  Run all inputs at once with 'source sbatch-all.sh'\n")
    else:
        print("  WARNING:  More than one *.sh file per folder. You should sbatch' them one by one.\n")


###########################################################################


def get_file(folder, extensions, preference=None):
    files = get_files(folder, extensions)
    if files is None:
        return None
    if len(files) > 1:
        for file in files:
            if preference in file:
                return file
        print("  ERROR:  "+folder+" contains too many "+extensions+" files, skipping...")
        return None
    return files[0]


def get_files(folder, extensions):
    files = os.listdir(folder)
    target_files = []
    if not isinstance(extensions, list):
        extensions = [extensions]
    for extension in extensions:
        for file in files:
            if file.endswith(extension):
                target_files.append(file)
        if target_files:
            return target_files
    return None


def count_files(folder, extension):
    files = get_files(folder, extension)
    if files is None:
        return 0
    return len(files)


def copy_as_newfile(template, new_file):
    with open(template, 'r') as template_file:
        template_content = template_file.readlines()
    with open(new_file, 'w') as new_file:
        new_file.writelines(template_content)
    return


def newfile_from_template(new_file, template):
    copy_as_newfile(template, new_file)
    with open(new_file, 'r') as file:
        lines = file.readlines()
    lines.insert(0, "! This file was created from '" + template + "' with " + version() + "\n")
    with open(new_file, 'w') as file:
        file.writelines(lines)


def delete_lines_between_keywords(key1, key2, filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()
    keep = []
    skip = False
    for line in lines:
        if key1 in line:
            skip = True
        if key2 in line:
            skip = False
        if not skip or key1 in line or key2 in line:
            keep.append(line)
    with open(filepath, 'w') as f:
        f.writelines(keep)


def add_lines_under_keyword(lines, keyword, filename):
    with open(filename, 'r') as file:
        document = file.readlines()
    index = next((i for i, line in enumerate(document) if line.strip().startswith(keyword)), None)
    if index is not None:
        for i, coord in enumerate(lines):
            document.insert(index + 1 + i, "        " + coord + "\n")
        with open(filename, 'w') as file:
            file.writelines(document)
    else:
        print("  ERROR:  Didn't find the '"+keyword+"' keyword in "+filename)


def replace_lines_under_keyword(lines, keyword, filename):
    with open(filename, 'r') as file:
        document = file.readlines()
    index = next((i for i, line in enumerate(document) if line.strip().startswith(keyword)), None)
    if index is not None:
        for i, row in enumerate(lines):
            if index + 1 + i < len(document):
                document[index + 1 + i] = row + "\n"
        with open(filename, 'w') as file:
            file.writelines(document)
    else:
        print("  ERROR:  Didn't find the '"+keyword+"' keyword in "+filename)


def replace_full_line_with_keyword(new_text, keyword, filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    with open(filename, 'w') as file:
        for line in lines:
            if keyword in line:
                line = new_text + '\n'
            file.write(line)
    return


def replace_str_on_keyword(new_text, keyword, filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    with open(filename, 'w') as file:
        for line in lines:
            if keyword in line:
                line = line.replace(keyword, new_text)
            file.write(line)
    return


def correct_psf(filename, fixing_psf):
    found_key = False
    with open(filename, 'r') as file:
        lines = file.readlines()
    for line in lines:
        for key in fixing_psf.keys():
            if key in line:
                found_key = True
                break
        if found_key:
            print("Correcting "+filename+"...")
            for key, value in fixing_psf.items():
                replace_str_on_keyword(value, key, filename)
            break
    return


def get_cell(structure_file):
    if old_inp_extension in structure_file:
        method = "get_cell_from_inp() of " + version()
        rows = get_cell_from_inp(structure_file)
    else:
        method = "get_cell_from_ase() of " + version()
        rows = get_cell_from_ase(structure_file)
    if rows == None or len(rows) != 3:
        print("  ERROR:  Didn't find the cell parameters in "+structure_file)
        return None

    cell = [None, None, None, None]
    cell[0] = "        A   " + rows[0]
    cell[1] = "        B   " + rows[1]
    cell[2] = "        C   " + rows[2]
    cell[3] = "        ! These cell parmeters were obtained from "+structure_file+" with the method "+method
    return cell


def get_cell_from_inp(inp_file_path):
    with open(inp_file_path, 'r') as inp_file:
        inp_content = inp_file.readlines()
    cell_rows = [None, None, None]
    for i, line in enumerate(inp_content):
        if line.strip() == '&CELL':
            for j in range(3):
                row = inp_content[i+j+1].strip()
                if row.startswith(('A ', 'B ', 'C ')):
                    cell_rows[j] = row[2:]
            return tuple(cell_rows)
    return None


def get_cell_from_ase(structure_file_path):
    try:
        structure = read(structure_file_path)
        cell = structure.cell[:]
        transposed_cell = zip(*cell)
        cell_rows = ["     ".join(f"{num:.15f}" for num in row) for row in transposed_cell]
        return tuple(cell_rows)
    except:
        return None


def get_coords(structure_file_path):
    try:
        structure = read(structure_file_path)
        symbols = structure.get_chemical_symbols()
        coords = structure.get_positions()
        coords_with_symbols = ["{} {:0.6f} {:0.6f} {:0.6f}".format(symbol, *coord) for symbol, coord in zip(symbols, coords)]
        coords_with_symbols.append('! These coordinates were obtained from '+structure_file_path+' with the method get_coords() of '+version())
        return coords_with_symbols
    except:
        print("  ERROR:  Didn't find the cell positions in "+structure_file)
        return None


def welcome_cp2k():
    print("")
    print("  ------------------------------------------------------------")
    print("  Welcome to " + version() + " for CP2K inputs.")
    print("  You should have already configured the '*.inp.template'")
    print("  and '*.sh.template' files, else check the README.md.")
    print("  ------------------------------------------------------------")
    print("  This is free software, and you are welcome to")
    print("  redistribute it under GNU General Public License.")
    print("  If you find this code useful, a citation would be awesome :D")
    print("  Pablo Gila-Herranz, “"+version()+"”, 2023.")
    print("  https://github.com/pablogila/input-maker")
    print("  ------------------------------------------------------------")
    print("")


###########################################################################


if __name__ == "__main__":
    cp2k()

