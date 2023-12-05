import os
import glob
try:
    from ase.io import read
except:
    print("ERROR: ASE package not found, install it with 'pip install ase'")
    exit()


############################################################
## Create CP2K input files from a template, easy piecy.
############################################################
##  Template and final input files.
##  The cell goes after this keyword in the template:
template_keyword_cell = '!KEYWORD_REPLACE_CELL_HERE'
template_keyword_coord = '!KEYWORD_COPY_POSITIONS_HERE'

template_init = 'templates/CP2K_MAPI_template-init.inp'
template_run = 'templates/CP2K_MAPI_template-run.inp'

final_file = 'CP2K_MAPI.inp'
##  For PDB, CELL or ASE-compatible files:
##  (Works better if you directly use the full filename)
cell_format = 'dumped.pdb'

psf_file = 'supercell-dump-1'
##  For already-existing INP input files, rename to .inp_ or
##  similar to avoid problems, mantaining the 'inp' string.
##  Also, the template must link to the PDB and PSF files.
#cell_format = '.inp_'
############################################################
# The psf file needs to be fixed for some weird reason.
fixing_psf_needed = True
fixing_psf = {
    'H       H     -99.000000' : 'H       H       0.023000',
    'C       C     -99.000000' : 'C       C       0.771000',
    'N       N     -99.000000' : 'N       N      -1.100000',
    'Pb      Pb    -99.000000' : 'Pb      Pb      2.030000',
    'I       I     -99.000000' : 'I       I      -1.130000',
    'D       D     -99.000000' : 'D       D       0.540000',
}


## @DEPRECATED
#  Use example:
#       if 'inp' in cell_format:
#           rows = cell_from_inp(structure_file_path)
#           # Must specify the PDB and PSF files in the template
#       else:
#           rows = cell_from_ase(structure_file_path)
#           coord = coords_from_ase(structure_file_path)
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


def coords_from_ase(structure_file_path):
    try:
        structure = read(structure_file_path)
        symbols = structure.get_chemical_symbols()
        coords = structure.get_positions()
        coords_with_symbols = ["{} {:0.6f} {:0.6f} {:0.6f}".format(symbol, *coord) for symbol, coord in zip(symbols, coords)]
        return coords_with_symbols
    except:
        print("ERROR: ASE can't read " + structure_file_path + ", skipping...")
        return None


## Read the template, insert the cell parameters, and save as new_file
def write_cell(template, new_file, rows):

    if not all(rows) and not len(rows) == 3:
        error_file = os.path.dirname(new_file)
        print("ERROR: Didn't find the cell parameters in " + error_file)
        return

    with open(template, 'r') as template_file:
        template_content = template_file.readlines()

    for i, line in enumerate(template_content):
        if line.strip() == template_keyword_cell:
            template_content[i+1] = "        A   " + rows[0] + "\n"
            template_content[i+2] = "        B   " + rows[1] + "\n"
            template_content[i+3] = "        C   " + rows[2] + "\n"

            print("Writting CELL in " + new_file)
            with open(new_file, 'w') as new_file:
                new_file.writelines(template_content)
            return
    print("ERROR: Didn't find the '" + template_keyword_cell + "' keyword")
    print("       in the '" + template + "' template.")


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


def correct_psf(filename):
    print("Fixing " + filename)
    with open(filename, 'r') as file:
        lines = file.readlines()
    with open(filename, 'w') as file:
        for line in lines:
            for key, value in fixing_psf.items():
                line = line.replace(key, value)
            file.write(line)


def main():
    # For each subfolder
    for folder in os.listdir('.'):

        if os.path.isdir(folder):
            new_file = os.path.join(folder, final_file)
            structure_file_path = glob.glob(os.path.join(folder, '*' + cell_format))

            if not structure_file_path: # Skip empty folders
                continue
            if len(structure_file_path) > 1:
                print("ERROR: More than one structural file found in " + folder + ", skipping...")
                continue
            structure_file_path = structure_file_path[0]

            rows = cell_from_ase(structure_file_path)
            coord = coords_from_ase(structure_file_path)

            psf_file_path = glob.glob(os.path.join(folder, '*' + psf_file))

            if not psf_file_path:
                # We will have to quickly run CP2K first to create the PSF file, then run again
                template = template_init
                write_cell(template, new_file, rows)
                write_coords(new_file, coord)
            else:
                # We can now run the full calculation
                template = template_run
                write_cell(template, new_file, rows)
                if fixing_psf_needed:
                    correct_psf(psf_file_path[0])
        
            if not psf_file_path:
                print("WARNING: No PSF file found. Run CP2K first to create it, then run again")


if __name__ == "__main__":
    main()

