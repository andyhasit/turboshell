import subprocess
from .vars import USER_INIT_FILE

def call(command):
    """
    Calls a command in an interactive shell so aliases are loaded.
    """
    # Don't set shell=True else it loads .bashrc (which we don't want)
    subprocess.call(['/bin/bash', '--rcfile', f'{USER_INIT_FILE}', '-ci', command])