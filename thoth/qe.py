'''
# Description
Functions to work with [Quantum ESPRESSO](https://www.quantum-espresso.org/).

# Index
- `readout()`
- `readin()`

---
'''


import pandas as pd
from .file import get
from .text import find
from .extract import number, string


def readout(file) -> pd.DataFrame:
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

    enery: float = None
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


def readin(file):
    '''
    Reads an input `file` from Quantum ESPRESSO,
    returning a Pandas dataframe with the input values used.
    > TODO: IMPLEMENT THIS
    '''
    pass

