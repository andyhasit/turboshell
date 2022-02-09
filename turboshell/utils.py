import os
import inspect
import sys
import subprocess


def error(msg):
    print(msg)
    sys.exit(1)


def write_to_file(path, lines):
    with open(path, 'w') as f:
        for line in lines:
            f.write(line + '\n')


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