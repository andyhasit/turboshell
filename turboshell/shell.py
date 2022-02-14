import subprocess

def call(command):
    """
    Calls a command in an interactive shell so aliases are loaded.
    """
    subprocess.call(['/bin/bash', '-i', '-c', command])

