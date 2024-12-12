'''
# Description
Functions to simplify calling bash scripts and related.

# Index
- `shell()`
- `git()`
- `here()`

---
'''


import subprocess
import datetime
import sys
import os


def shell(command, cwd=None):
    '''
    Run a shell `command`, inside an optional `cwd` directory.
    If empty, the current working directory will be used.
    Returns the result of the command used.
    '''
    result = subprocess.run(command, shell=True, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print('>>>  ' + command)
    return result


def git(path=None) -> None:
    '''Update'''
    if path:
        os.chdir(path)
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    # Fetch the latest changes from the remote repository
    shell("git fetch")
    # Check if the local repository is behind the remote repository
    rev_list_result = shell("git rev-list HEAD...origin/master --count")
    rev_list_output = rev_list_result.stdout.strip()
    if rev_list_output:
        if int(rev_list_output) != 0:
            raise RuntimeError("Changes detected in the remote repository. Check it manually...")
    # Stage and commit changes
    shell("git add .")
    commit_result = shell(f'git commit -m "Automatic push on {date} with Thoth {version}"')
    if commit_result.returncode != 0:
        raise RuntimeError("Git commit failed. Check it manually...")
    # Push changes to the remote repository
    push_result = shell("git push")
    if push_result.returncode != 0:
        raise RuntimeError("Git push failed. Check it manually...")
    print("Git updated!")
    return None


def here(run_here=True):
    '''
    Returns the directory where the current script lies.
    By default, it also runs the rest of the script from said directory;
    This is really useful to run scripts from the VSCode terminal, etc.
    You might want to override this behaviour if you just want to know the path of the current script;
    to do so, set `run_here=False`.
    '''
    caller = os.path.dirname(os.path.abspath(os.path.realpath(sys.argv[0])))
    if run_here:
        os.chdir(caller)
    return caller

