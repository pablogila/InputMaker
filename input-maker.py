import os
import glob
try:
    from ase.io import read
except:
    print("ERROR: ASE package not found, install it with 'pip install ase'")
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



def cp2k():

    path = os.getcwd()

    inp_template = get_file(path, '.inp.template')
    slurm_template = get_file(path, '.sh.template')

    if inp_template is None:
        print("ERROR:  No '*.inp.template' input found in path, exiting...")
        exit()
    new_inp_name = inp_template.replace('.template','')

    if slurm_template is None:
        print("WARNING:  No '*.sh.template' slurm template found in path, you will have to run manually")
        new_slurm_name = None
    else:
        new_slurm_name = slurm_template.replace('.template','')

    # Main loop
    for folder in os.listdir('.'):
        if os.path.isdir(folder):

            structure_file = get_file(folder, structure_extensions, preferred_structure_file)
            if structure_file is None:
                continue

            new_inp_path = os.path.join(folder, new_inp_name)

            psf_file = get_file(folder, '.psf')
            pdb_file = get_file(folder, '.pdb', preferred_structure_file)

            cell = get_cell(structure_file)
            if cell is None:
                continue
            replace_lines_under_keyword(cell, key_cell, new_inp_path) # TO-DO

            if slurm_template:
                new_slurm_path = os.path.join(folder, new_slurm_name)
                new_file_from_template(new_slurm_path, slurm_template) # TO-DO
                replace_keyword(key_jobname, folder, new_slurm_path)
                replace_keyword(key_filename, new_inp_name.replace('.inp', ''), new_slurm_path)

            if not psf_file: # 1st run
                positions = get_coords(structure_file)
                if positions is None:
                    continue
                new_file_from_template(new_inp_name, inp_template) # TO-DO
                delete_lines_between_keywords(key_topology_run, key_topology_end, new_inp_path) # TO-DO
                add_lines_under_keyword(positions, key_coordinates, new_inp_path) # TO-DO
                replace_lines_under_keyword(['    STEPS 1'], key_steps, new_inp_path)

                if slurm_template:
                    replace_full_line_with_keyword('#SBATCH --time=00:02:00', '#SBATCH --time=', new_slurm_path)

            else: # 2nd run
                new_file_from_template(new_inp_name, inp_template) # TO-DO
                delete_lines_between_keywords(key_topology_init, key_topology_run, new_inp_path)
                replace_lines_under_keyword(['        COORD_FILE_NAME ./' + pdb_file], key_pdb_filename, new_inp_path)
                replace_lines_under_keyword(['        CONN_FILE_NAME ./' + psf_file], key_psf_filename, new_inp_path)

                correct_psf(psf_file, fixing_psf)


###########################################################################


def get_file(folder, extensions, preference=None):
    files = get_files(folder, extensions)
    if files is None:
        return None
    if len(files) > 1:
        for file in files:
            if preference in file:
                return file
        print("ERROR: {folder} contains too many {extensions} files, skipping...")
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


def new_file_from_template(new_file, template):
    pass
def delete_lines_between_keywords(key1, key2, file):
    pass
def add_lines_under_keyword(lines, key, file): # from write_positions
    pass
def replace_lines_under_keyword(lines, key, file): # from write_cell
    pass
def replace_full_line_with_keyword(new_text, key, file):
    pass


def replace_keyword(key, new_text, file):
    with open(file, 'r') as file:
        lines = file.readlines()
    with open(file, 'w') as file:
        for line in lines:
            if key in line:
                line = line.replace(key, new_text)
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
            print("Correcting {filename}...")
            for key, value in fixing_psf.items():
                replace_keyword(key, value, filename)
            break
    return


def get_cell(structure_file):
    if old_inp_extension in structure_file:
        rows = get_cell_from_inp(structure_file)
    else:
        rows = get_cell_from_ase(structure_file)
    if rows == None or len(rows) != 3:
        print("ERROR:  Didn't find the cell parameters in {structure_file}")
        return None
    cell = []
    cell[0] = "        A   " + rows[0]
    cell[1] = "        B   " + rows[1]
    cell[2] = "        C   " + rows[2]
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
        return coords_with_symbols
    except:
        print("ERROR:  Didn't find the cell positions in {structure_file}")
        return None






"""

# DEPRECATED
## Read the template, insert the cell parameters, and save as new_file
def write_cell(template, new_file, rows):

    if not all(rows) and not len(rows) == 3:
        error_file = os.path.dirname(new_file)
        print("ERROR:  Didn't find the cell parameters in " + error_file)
        return

    with open(template, 'r') as template_file:
        template_content = template_file.readlines()

    for i, line in enumerate(template_content):
        if line.strip() == key_cell:
            template_content[i+1] = "        A   " + rows[0] + "\n"
            template_content[i+2] = "        B   " + rows[1] + "\n"
            template_content[i+3] = "        C   " + rows[2] + "\n"

            print("Writting CELL in " + new_file)
            with open(new_file, 'w') as new_file:
                new_file.writelines(template_content)
            return
    print("ERROR:  Didn't find the {key_cell} keyword")
    print("        in the '" + template + "' template.")


## Open the already-written file and insert the coordinates
def write_coords(new_file, coordinates):
    with open(new_file, 'r') as file:
        lines = file.readlines()
    index = next((i for i, line in enumerate(lines) if line.strip().startswith(template_keyword_coord)), None)
    if index is not None:
        print("Writting COORD in " + new_file)
        for i, coord in enumerate(coordinates):
            lines.insert(index + 1 + i, "        " + coord + "\n")
        with open(new_file, 'w') as file:
            file.writelines(lines)
    else:
        print(f"ERROR: Didn't find the '{template_keyword_coord}' keyword in the input template.")


""""



if __name__ == "__main__":
    cp2k()

