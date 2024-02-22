import os
import sys
try:
    from ase.io import read
except:
    print("  WARNING: ASE package not found, install it with 'pip install ase'")


def version():
    return 'v.2024.02.22.1600'


def name():
    return 'InputMaker'


def castep(supercell, custom_out_folder = None):

    print("")
    print("  -------------------------------------------------------------")
    print("  Welcome to " + name() + " " + version() + " for CASTEP inputs.")
    print("  -------------------------------------------------------------")
    print("  This is free software, and you are welcome to")
    print("  redistribute it under GNU General Public License.")
    print("  If you find this code useful, a citation would be awesome :D")
    print("  Pablo Gila-Herranz, “" + name() + "” " + version() + ", 2024.")
    print("  https://github.com/pablogila/InputMaker")
    print("  -------------------------------------------------------------")
    print("")

    if supercell == None:
        supercell_call = ""

    else:
        if not supercell.startswith('[') or not supercell.endswith(']'):
            print("  ERROR: supercell argument must be given as [k,l,m]. Try again...\n")
            exit()
        supercell_call = " --supercell=" + supercell
        
    path = os.getcwd()
    cif_files = get_files(path, '.cif')

    if custom_out_folder == None:
        out_folder = ""
    else:
        if not os.path.exists(custom_out_folder):
            os.makedirs(custom_out_folder)
        out_folder = custom_out_folder + "/"

    if cif_files is not None:
        for cif_file in cif_files:
            output_name = cif_file.replace('.cif', '.cell')
            command = 'cif2cell ' + cif_file + ' -p castep ' + supercell_call + ' -o ' + out_folder + output_name
            os.system(command)
            #command = ['cif2cell', cif_file, '-p', 'castep', supercell_call, '-o', output_name]
            #subprocess.call(command)
            print("  " + command)
    else:
        for folder in os.listdir('.'):
            if os.path.isdir(folder):
                if custom_out_folder == None:
                    out_folder = folder + "/"
                cif_file = get_file(folder, ".cif")
                if cif_file is None:
                    continue
                output_name = cif_file.replace('.cif', '.cell')
                command = 'cif2cell ' + folder + "/" + cif_file + ' -p castep ' + supercell_call + ' -o ' + out_folder + output_name
                os.system(command)
                #command = ['cif2cell', cif_file, '-p', 'castep', supercell_call, '-o', output_name]
                #subprocess.call(command)
                print("  " + command)
    print("")
    print("  Done!\n")


def cp2k():
    ###########################################################################
    ## Create CP2K input files from a template, easy piecy.
    ###########################################################################
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

    print("")
    print("  -------------------------------------------------------------")
    print("  Welcome to " + name() + " " + version() + " for CP2K inputs.")
    print("  You should have already configured the '*" + inp_template_extension + "'")
    print("  and '*" + slurm_template_extension + "' files, else check the README.md.")
    print("  -------------------------------------------------------------")
    print("  This is free software, and you are welcome to")
    print("  redistribute it under GNU General Public License.")
    print("  If you find this code useful, a citation would be awesome :D")
    print("  Pablo Gila-Herranz, “" + name() + "” " + version() + ", 2024.")
    print("  https://github.com/pablogila/InputMaker")
    print("  -------------------------------------------------------------")
    print("")

    path = os.getcwd()
    inp_template = get_file(path, inp_template_extension)
    slurm_template = get_file(path, slurm_template_extension)

    if inp_template is None:
        print("  ERROR: No '*" + inp_template_extension + "' input found in path, exiting...\n")
        exit()
    new_inp_name = inp_template.replace(inp_template_extension, '.inp')

    if slurm_template is None: # Warning will be printed at the end
        new_slurm_name = None
    else:
        new_slurm_name = slurm_template.replace(slurm_template_extension, '.sh')

    for folder in os.listdir('.'):
        if os.path.isdir(folder):

            structure_name = get_file(folder, structure_extensions, preferred_structure_file)
            if structure_name is None:
                continue
            else:
                structure_file = os.path.join(folder, structure_name)

            new_inp_path = os.path.join(folder, new_inp_name)

            psf_file = get_file(folder, '.psf', preferred_psf_file)
            pdb_file = get_file(folder, '.pdb', preferred_structure_file)

            cell = get_cell(structure_file)
            if cell is None:
                continue

            template_to_newfile(inp_template, new_inp_path, "! This file was created from " + inp_template + " with " + name() + " " + version())

            replace_lines_under_keyword(cell, key_cell, new_inp_path)

            if not psf_file: # 1st run
                is_first_run_needed = True # Raise a warning flag
                positions = get_coords(structure_file)
                if positions is None:
                    continue
                template_to_newfile(new_inp_path, new_inp_path, "! WARNING: Perform a first run of CP2K to create the *.psf file, then run again " + name() + " and CP2K.")
                delete_lines_between_keywords(key_topology_run, key_topology_end, new_inp_path)
                add_lines_under_keyword(positions, key_coordinates, new_inp_path)
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


###########################################################################
#    COMMON FUNCTIONS
###########################################################################


def get_file(folder, extensions, preference=None):
    files = get_files(folder, extensions)
    if files is None:
        return None
    if len(files) > 1:
        for file in files:
            if preference in file:
                return file
        print("  ERROR: " + folder + " contains too many " + extensions + " files, skipping...")
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


def template_to_newfile(template, new_file, comment):
    copy_as_newfile(template, new_file)
    with open(new_file, 'r') as file:
        lines = file.readlines()
    lines.insert(0, comment + "\n")
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
        print("  ERROR:  Didn't find the '" + keyword + "' keyword in " + filename)


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
        print("  ERROR: Didn't find the '" + keyword + "' keyword in " + filename)


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


def correct_file_with_dict(filename, fixing_dict):
    found_key = False
    with open(filename, 'r') as file:
        lines = file.readlines()
    for line in lines:
        for key in fixing_dict.keys():
            if key in line:
                found_key = True
                break
        if found_key:
            print("  Correcting " + filename + "...")
            for key, value in fixing_dict.items():
                replace_str_on_keyword(value, key, filename)
            break
    return


def get_cell(structure_file, alternate_extension = '.inp.old'):
    if alternate_extension in structure_file:
        method = "get_cell_from_inp() of " + name() + " " + version()
        rows = get_cell_from_inp(structure_file)
    else:
        method = "get_cell_from_ase() of " + name() + " " + version()
        rows = get_cell_from_ase(structure_file)
    if rows == None or len(rows) != 3:
        print("  ERROR: Didn't find the cell parameters in " + structure_file)
        return None

    cell = [None, None, None, None]
    cell[0] = "        A   " + rows[0]
    cell[1] = "        B   " + rows[1]
    cell[2] = "        C   " + rows[2]
    cell[3] = "        ! These cell parameters were obtained from " + structure_file + " with the method " + method
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
        coords_with_symbols.append("! These positions were obtained from " + structure_file_path + " with the method get_coords() of " + name() + " " + version())
        return coords_with_symbols
    except:
        print("  ERROR: Didn't find the cell positions in " + structure_file_path)
        return None


def rename_files_on_subfolders(old_extension, new_extension):
    for folder in os.listdir('.'):
        if os.path.isdir(folder):
            for file in os.listdir(folder):
                if file.endswith(old_extension):
                    old_file = os.path.join(folder, file)
                    new_file = os.path.join(folder, file.replace(old_extension, new_extension))
                    os.rename(old_file, new_file)


###########################################################################


if __name__ == "__main__":

    if '-cp2k' in sys.argv or '-CP2K' in sys.argv or 'cp2k' in sys.argv or 'CP2K' in sys.argv:
        cp2k()

    elif '-castep' in sys.argv or '-CASTEP' in sys.argv or 'castep' in sys.argv or 'CASTEP' in sys.argv:

        if 'out' in sys.argv or 'OUT' in sys.argv or '-out' in sys.argv or '-OUT' in sys.argv or '--out' in sys.argv or '--OUT' in sys.argv:
            out_folder = 'out'
        else:
            out_folder = None

        supercell = None
        for arg in sys.argv:
            if arg.startswith(('--supercell=', '-supercell=', 'supercell=', '--SUPERCELL=', '-SUPERCELL=', 'SUPERCELL=')):
                supercell = arg.split('=')[1]
                break

        castep(supercell, out_folder)

