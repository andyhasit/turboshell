import subprocess
from .vars import USER_INIT_FILE

def call(command):
    """
    Calls a command in an interactive shell so aliases are loaded.
    """
    # Don't set shell=True else it loads .bashrc (which we don't want)

    #subprocess.call(['/bin/bash', '-i', '-c', command])
    #subprocess.call(['/bin/bash', '--rcfile', f'{USER_INIT_FILE}', '-c', command.split(" ")])
    #subprocess.call(f"{command}", executable=f"/bin/bash --init-file {USER_INIT_FILE}", shell=True)

    #subprocess.call(['/bin/bash', '--rcfile', f'{USER_INIT_FILE}', '-c', command])
    # subprocess.call(['/bin/bash', '-c', f"/bin/bash --rcfile {USER_INIT_FILE};{command}"])
    #subprocess.call(['/bin/bash', '--rcfile', f'{USER_INIT_FILE}', '-c', command])

    subprocess.call(['/bin/bash', '--rcfile', f'{USER_INIT_FILE}', '-c', command])