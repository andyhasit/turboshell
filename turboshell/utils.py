import os
import sys
import subprocess


TURBOSHELL_USER_DIR = os.environ.get('TURBOSHELL_USER_DIR')


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
