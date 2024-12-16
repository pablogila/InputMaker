'''
# Description
Functions to work with [Quantum ESPRESSO](https://www.quantum-espresso.org/) calculation files.

# Index
- `read_in()`
- `read_out()`
- `read_dir()`
- `read_dirs()`

---
'''


import pandas as pd
import os
from .file import get, get_list
from .text import find
from .extract import number, string


def read_in(file) -> pd.DataFrame:
    '''
    Reads an input `file` from Quantum ESPRESSO,
    returning a Pandas DataFrame with the input values used.
    The columns are named after the name of the corresponding variable.
    '''
    file = get(file)
    data = {}
    lines = find('=', file)
    for line in lines:
        line.strip()
        var, value = line.split('=', 1)
        var = var.strip()
        value = value.strip()
        if var.startswith('!'):
            continue
        try:
            value_float = value.replace('d', 'e')
            value_float = value_float.replace('D', 'e')
            value_float = value_float.replace('E', 'e')
            value_float = float(value_float)
            value = value_float
        except ValueError:
            pass # Then it is a string
        data[var] = value
    # Get values that are not expressed with a '=' sign
    k_points = find('K_POINTS', file, -1, 1, True)
    if k_points:
        k_points = k_points[1].strip()
        data['K_POINTS'] = k_points
    return pd.DataFrame.from_dict([data])


def read_out(file) -> pd.DataFrame:
    '''
    Reads an output `file` from Quantum ESPRESSO,
    returning a Pandas DataFrame with the following columns:
    `'Energy'` (float), `'Total force'` (float), `'Total SCF correction'` (float),
    `'Runtime'` (str), `'JOB DONE'` (bool), `'BFGS converged'` (bool), `'BFGS failed'` (bool),
    `'Maxiter reached'` (bool), `'Error'` (str), `'Success'` (bool).
    '''
    file = get(file)

    energy_key           = '!    total energy'
    force_key            = 'Total force'
    scf_key              = 'Total SCF correction'
    time_key             = 'PWSCF'
    time_stop_key        = 'CPU'
    job_done_key         = 'JOB DONE.'
    bfgs_converged_key   = 'bfgs converged'
    bfgs_failed_key      = 'bfgs failed'
    maxiter_reached_key  = 'Maximum number of iterations reached'
    error_key            = 'Error in routine'

    energy_line          = find(energy_key, file, -1)
    force_line           = find(force_key, file, -1)
    time_line            = find(time_key, file, -1)
    job_done_line        = find(job_done_key, file, -1)
    bfgs_converged_line  = find(bfgs_converged_key, file, -1)
    bfgs_failed_line     = find(bfgs_failed_key, file, -1)
    maxiter_reached_line = find(maxiter_reached_key, file, -1)
    error_line           = find(error_key, file, -1, 1, True)

    energy: float = None
    force: float = None
    scf: float = None
    time: str = None
    job_done: bool = False
    bfgs_converged: bool = False
    bfgs_failed: bool = False
    maxiter_reached: bool = False
    error: str = ''
    success: bool = False

    if energy_line:
        energy = number(energy_line[0], energy_key)
    if force_line:
        force = number(force_line[0], force_key)
        scf = number(force_line[0], scf_key)
    if time_line:
        time = string(time_line[0], time_key, time_stop_key)
    if job_done_line:
        job_done = True
    if bfgs_converged_line:
        bfgs_converged = True
    if bfgs_failed_line:
        bfgs_failed = True
    if maxiter_reached_line:
        maxiter_reached = True
    if error_line:
        error = error_line[1].strip()
    if job_done and not bfgs_failed and not maxiter_reached and not error:
        success = True

    output = {
        'Energy'                : energy,
        'Total force'           : force,
        'Total SCF correction'  : scf,
        'Runtime'               : time,
        'JOB DONE'              : job_done,
        'BFGS converged'        : bfgs_converged,
        'BFGS failed'           : bfgs_failed,
        'Maxiter reached'       : maxiter_reached,
        'Error'                 : error,
        'Success'               : success,
    }
    return pd.DataFrame.from_dict([output])


def read_dir(folder, input_str:str='.in', output_str:str='.out') -> pd.DataFrame:
    '''
    Takes a `folder` containing a Quantum ESPRESSO calculation,
    and returns a Pandas DataFrame containing the input parameters and output results.
    Input and output files are determined automatically,
    but must be specified with `input_str` and `output_str` if more than one file ends with `.in` or `.out`.
    To extract values only from the input or only from the output, check `read_in()` and `read_out()`.
    '''
    input_file = get(folder, input_str)
    output_file = get(folder, output_str)
    if not input_file:
        print(f'Skipping due to input file missing at {folder}')
        return None
    if not output_file:
        print(f'Skipping due to output file missing at {folder}')
        return None
    df_out = read_out(output_file)
    df_in = read_in(input_file)
    df = df_out.join(df_in)
    return df


def read_dirs(directory, input_str:str='.in', output_str:str='.out', calc_splitter='_', calc_type_index=0, calc_id_index=1):
    '''
    Calls recursively `read_dir()`, reading Quantum ESPRESSO calculations
    from all the subfolders inside the given `directory`.
    The results are saved to CSV files inside the current directory.
    Input and output files are determined automatically, but must be specified with
    `input_str` and `output_str` if more than one file ends with `.in` or `.out`.

    To properly group the calculations per type, saving separated CSVs for each calculation type,
    you can modify `calc_splitter` ('_' by default), `calc_type_index` (0) and `calc_id_index` (1).
    With these default values, a subfolder named './CalculationType_CalculationID_AdditionalText/'
    will be interpreted as follows:
    - Calculation type: 'CalculationType' (The output CSV will be named after this)
    - CalculationID: 'CalculationID' (Stored in the 'ID' column of the resulting dataframe)

    If everything fails, the subfolder name will be used.
    '''
    print(f'Reading all Quantum ESPRESSO calculations from {directory} ...')
    folders = get_list(directory)
    if not folders:
        raise FileNotFoundError('The directory is empty!')
    # Separate calculations by their title in an array
    calc_types = []
    folders.sort()
    for folder in folders:
        if not os.path.isdir(folder):
            folders.remove(folder)
            continue
        folder_name = os.path.basename(folder)
        try:
            calc_name = folder_name.split(calc_splitter)[calc_type_index]
        except:
            calc_name = folder_name
        if not calc_name in calc_types:
            calc_types.append(calc_name)
    len_folders = len(folders)
    total_success_counter = 0
    for calc in calc_types:
        len_calcs = 0
        success_counter = 0
        results = pd.DataFrame()
        for folder in folders:
            if not calc in folder:
                continue
            len_calcs += 1
            folder_name = os.path.basename(folder)
            try:
                calc_id = folder_name.split(calc_splitter)[calc_id_index]
            except:
                calc_id = folder_name
            df: pd.DataFrame = read_dir(folder, input_str, output_str)
            if df is None:
                continue
            df.insert(0, 'ID', calc_id)
            df = df.dropna(axis=1, how='all')
            results = pd.concat([results, df], axis=0, ignore_index=True)
            if df['Success'][0]:
                success_counter += 1
                total_success_counter += 1
        results.to_csv(os.path.join(directory, calc+'.csv'))
        print(f'Saved to CSV: {calc} ({success_counter} successful calculations out of {len_calcs})')
    print(f'Total successful calculations: {total_success_counter} out of {len_folders}')

