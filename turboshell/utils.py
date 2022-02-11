import os
import inspect
import sys
import subprocess
from .vars import CMD_SEP


def split_cmd_shortcut(cmd):
    """
    Splits a cmd shortcut into chunks:

        n.p.a     >   ['n', 'p', 'a']
        .npa      >   ['n', 'p', 'a']
        n.pa      >   ['n', 'pa']
        .n.pa     >   ['n', 'pa']

    """
    final = []
    chunks = cmd.split(CMD_SEP)
    splitnext = False
    for chunk in chunks:
        if splitnext:
            for c in chunk:
                final.append(c)
            splitnext = False
            continue
        if chunk == '':
            splitnext = True
        else:
            final.append(chunk)
            splitnext = False
    return final


def print_instructions():
    print('Type ts.info for a list of commands.')


def is_empty(var):
    """
    Returns True if a variable is None or an empty string.
    """
    if var is None:
        return True
    if isinstance(var, str):
        return len(var.strip()) == 0


def error(msg):
    print(msg)
    sys.exit(1)


def write_to_file(path, lines):
    with open(path, 'w') as f:
        for line in lines:
            f.write(line + '\n')
            #print(line)


def ensure_dir_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)


def call(cmd, shell=True, executable='/bin/bash'):
    return subprocess.call(cmd, shell, executable)


def extract_stubs(alias):
    combinations = []
    current = ''
    for bit in alias.split('.')[:-1]:
        current += bit + '.'
        combinations.append(current)
    return combinations


def get_full_name(func):
    return inspect.getmodule(func).__name__ + '.' + func.__name__