import os
import glob
from ase.io import read


############################################################
## Create CP2K input files from a template, easy piecy.
############################################################
##  Template and final input files.
##  The cell goes after this keyword in the template:
template_cell_keyword = '!REPLACE_CELL_HERE' 
template = 'CP2K_MAPI_template.inp'
final_file = 'CP2K_MAPI.inp'
##  For PDB, CELL or ASE-compatible files:
cell_format = '.pdb'
##  For already-existing INP input files, rename to .inp_ or
##  similar to avoid problems, mantaining the 'inp' string:
#cell_format = '.inp_'
############################################################


def cell_from_inp(inp_file_path):

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


def cell_from_ase(structure_file_path):
    try:
        structure = read(structure_file_path)
        cell = structure.cell[:]
        transposed_cell = zip(*cell)
        cell_rows = ["     ".join(f"{num:.15f}" for num in row) for row in transposed_cell]
        return tuple(cell_rows)
    except:
        print("ERROR: ASE can't read " + structure_file_path + ", skipping...")
        return None


def write_cell(template, new_file, rows):

    if not all(rows) and not len(rows) == 3:
        error_file = os.path.dirname(new_file)
        print("ERROR: Didn't find the cell parameters in " + error_file)
        return

    with open(template, 'r') as template_file:
        template_content = template_file.readlines()

    for i, line in enumerate(template_content):
        if line.strip() == template_cell_keyword:
            template_content[i+1] = "        A   " + rows[0] + "\n"
            template_content[i+2] = "        B   " + rows[1] + "\n"
            template_content[i+3] = "        C   " + rows[2] + "\n"

            print("Writting input in " + new_file)
            with open(new_file, 'w') as new_file:
                new_file.writelines(template_content)
            return
    print("ERROR: Didn't find the '" + template_cell_keyword + "' keyword")
    print("       in the '" + template + "' template.")


def main():
    # For each subfolder
    for folder in os.listdir('.'):

        if os.path.isdir(folder):
            new_file = os.path.join(folder, final_file)
            structure_file_path = glob.glob(os.path.join(folder, '*' + cell_format))

            if not structure_file_path: # Skip empty folders
                continue
            if len(structure_file_path) > 1:
                print("ERROR: More than one input found in " + folder + ", skipping...")
                continue
            structure_file_path = structure_file_path[0]

            if 'inp' in cell_format:
                rows = cell_from_inp(structure_file_path)
            else:
                rows = cell_from_ase(structure_file_path)

            write_cell(template, new_file, rows)


if __name__ == "__main__":
    main()

