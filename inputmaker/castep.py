'''
# Description
This module is supposed to handle the creation of CASTEP input files.
Still under heavy development.

# Index
- `castep()`

---
'''

from . import tools

def castep(supercell = None, custom_out_folder = None, move_to_subfolders = False):
    '''
    Create CASTEP input files from CIF files.
    This function is still under heavy development.
    '''

    print(tools.welcome('CASTEP'))

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

    # If CIF files are in the main folder:
    if cif_files is not None:
        for cif_file in cif_files:
            output_name = cif_file.replace('.cif', '.cell')
            command = 'cif2cell ' + cif_file + ' -p castep ' + supercell_call + ' -o ' + out_folder + output_name
            os.system(command)
            print("  " + command)
        if move_to_subfolders:
            copy_files_to_subfolders('.cell')
            print("  Copied all CASTEP inputs to individual subfolders.")

    # If CIF files are in subfolders:
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
                print("  " + command)
    print("")
    print("  Done!\n")
