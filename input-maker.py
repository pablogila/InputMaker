import os
import glob


####################################################
# This script copies the cell parameters from the CP2K input files
####################################################
# Template and final input files:
template = 'CP2K_MAPI_template.inp'
template_cell_keyword = '!REPLACE_CELL_HERE' # The cell goes after this string in the template
final_file = 'CP2K_MAPI.inp'
# For already-existing INP input files, please rename the extension
cell_format = '.inp_' # Whatever, just rename the INP extension
cell_keyword = '&CELL'
# Or for CELL files: STILL NOT SUPPORTED
# cell_format = '.cell'
# cell_keyword = '%BLOCK LATTICE_CART'
# TO-DO: USE ASE TO READ PDB AND GET THE CELL PARAMETERS
####################################################


def cell_from_inp(inp_file_path):

    with open(inp_file_path, 'r') as inp_file:
        inp_content = inp_file.readlines()
    a_row = b_row = c_row = None

    for i, line in enumerate(inp_content):
        if line.strip() == cell_keyword:
            a_row = inp_content[i+1].strip() if inp_content[i+1].strip().startswith('A ') else None
            a_row = a_row[2:]
            b_row = inp_content[i+2].strip() if inp_content[i+2].strip().startswith('B ') else None
            b_row = b_row[2:]
            c_row = inp_content[i+3].strip() if inp_content[i+3].strip().startswith('C ') else None
            c_row = c_row[2:]

        if all([a_row, b_row, c_row]):
            return a_row, b_row, c_row


def write_cell(template, new_file, a_row, b_row, c_row):

    with open(template, 'r') as template_file:
        template_content = template_file.readlines()

    for i, line in enumerate(template_content):
        if line.strip() == template_cell_keyword:
            template_content[i+1] = "        A " + a_row + "\n"
            template_content[i+2] = "        B " + b_row + "\n"
            template_content[i+3] = "        C " + c_row + "\n"

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
            inp_file_path = glob.glob(os.path.join(folder, '*' + cell_format))

            if not inp_file_path: # Skip empty folders
                continue
            if len(inp_file_path) > 1:
                print("ERROR: More than one input found in " + folder + ", skipping...")
                continue
            inp_file_path = inp_file_path[0]

            a_row, b_row, c_row = cell_from_inp(inp_file_path)
            if not all([a_row, b_row, c_row]):
                print("ERROR: Didn't find the cell parameters in " + inp_file_path)
                continue

            write_cell(template, new_file, a_row, b_row, c_row)


if __name__ == "__main__":
    main()

