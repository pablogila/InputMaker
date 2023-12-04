import os
import glob

####################################################
# This script copies the cell parameters from the CP2K input files
####################################################
# Template and final input files:
template = 'CP2K_MAPI_template.inp'
final_file = 'CP2K_MAPI.inp'
# For already-existing INP input files, please rename the extension
cell_format = '.inp_' # Whatever, just rename the INP extension
cell_keyword = '&CELL'
# Or for CELL files: STILL NOT SUPPORTED
# cell_format = '.cell'
# cell_keyword = '%BLOCK LATTICE_CART'
# TO-DO: USE ASE TO READ PDB AND GET THE CELL PARAMETERS
####################################################


# Open the template file and read its content
with open(template, 'r') as template_file:
    template_content = template_file.readlines()

# For each subfolder
for folder in os.listdir('.'):
    if os.path.isdir(folder):
        inp_file_path = glob.glob(os.path.join(folder, '*' + cell_format))
        if not inp_file_path:
            continue
        inp_file_path = inp_file_path[0]

        with open(inp_file_path, 'r') as inp_file:
            inp_content = inp_file.readlines()

        # Extract the A, B, and C rows only if they are preceded by $CELL
        a_row = b_row = c_row = None
        for i, line in enumerate(inp_content):
            if line.strip() == cell_keyword:
                a_row = inp_content[i+1].strip() if inp_content[i+1].strip().startswith('A ') else None
                b_row = inp_content[i+2].strip() if inp_content[i+2].strip().startswith('B ') else None
                c_row = inp_content[i+3].strip() if inp_content[i+3].strip().startswith('C ') else None
            if all([a_row, b_row, c_row]):
                break  # Stop looking for CELL

        if not all([a_row, b_row, c_row]):
            print("ERROR: Didn't find the cell parameters in ", folder)
            continue  # Skip this file if A, B, or C row is missing

        # Replace the A, B, and C rows in the template content
        a_done = b_done = c_done = False
        for i, line in enumerate(template_content):
            if line.strip() == '&CELL':
                if template_content[i+1].strip().startswith('A '):
                    template_content[i+1] = "        " + a_row + "\n"
                    a_done = True
                if template_content[i+2].strip().startswith('B '):
                    template_content[i+2] = "        " + b_row + "\n"
                    b_done = True
                if template_content[i+3].strip().startswith('C '):
                    template_content[i+3] = "        " + c_row + "\n"
                    c_done = True
            if all([a_done, b_done, c_done]):
                print("Copied cell in ", folder)
                break  # Stop looking for CELL

        # Write the modified content to a new file in the subfolder
        with open(os.path.join(folder, final_file), 'w') as new_file:
            new_file.writelines(template_content)

