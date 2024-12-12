'''
# Description
Functions to work with [Quantum ESPRESSO](https://www.quantum-espresso.org/) calculation files.

# Index
- `read_in()`
- `read_out()`
- `read_dir()`

---
'''


import pandas as pd
from .file import get
from .text import find
from .extract import number, string


def read_in(file):
    '''
    Reads an input `file` from Quantum ESPRESSO,
    returning a Pandas DataFrame with the input values used.
    '''
    file = get(file)
    data = {}
    lines = find('=', file)
    for line in lines:
        line.strip()
        if line.startswith('!'):
            continue
        var, value = line.split('=', 1)
        var = var.strip()
        value = value.strip()
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
    return pd.DataFrame.from_dict(data)


def read_out(file) -> pd.DataFrame:
    '''
    Reads an output `file` from Quantum ESPRESSO,
    returning a Pandas DataFrame with the following columns:
    `'Energy'`, `'Total force'`, `'Total SCF correction'`, `'Runtime'`, `'JOB DONE'`, `'BFGS converged'`, `'BFGS failed'`, `'Maxiter reached'`, `'Error'`.
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

    if energy_line:
        energy = number(energy_line[0], energy_key)
    if force_line:
        force = number(force_line[0], force_key)
        scf = number(force_line[0], scf_key)
    if time_line:
        time = string(time_line, time_key, time_stop_key)
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
    }
    return pd.DataFrame.from_dict(output)


def read_dir(folder, input='.in', output='.out'):
    '''
    Takes a `folder` containing a Quantum ESPRESSO calculation,
    and returns a Pandas DataFrame containing the input parameters and output results.
    The `input` and `output` files are determined automatically,
    but must be specified if more than one file ends with `.in` or `.out`.
    To extract values only from the input or only from the output, check `read_in` and `read_out`.
    '''
    input_file = get(folder, input)
    output_file = get(folder, output)
    if not input_file:
        raise FileNotFoundError(f'Input file missing at {folder}')
    if not output_file:
        raise FileNotFoundError(f'Output file missing at {folder}')
    if len(input_file) > 1:
        raise ValueError(f'Please specify an input name! More than 1 input file found in {folder}')
    if len(output_file) > 1:
        raise ValueError(f'Please specify an output name! More than 1 output file found in {folder}')
    input_file = input_file[0]
    output_file = output_file[0]
    df_in = read_in(input_file)
    df_out = read_out(output_file)
    df = pd.merge(df_in, df_out)
    return df

