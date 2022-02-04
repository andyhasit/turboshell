"""
This module gets run when you call "python -m turboshell"
"""

import os
import sys
from .utils import error, TURBOSHELL_USER_DIR
from .turboshell import ts
from .constants import REBUILD_CMD
# The following import collects the commands and aliases
from . import builtin_cmds  # noqa


def call_command(argv):
    """
    Calls a custom (user-defined) command.
    """
    try:
        cmd_name = argv[1]
        cmd_args = argv[2:]
    except IndexError:
        error('Use: "python -m turboshell cmd-name [...args]"')

    if TURBOSHELL_USER_DIR and os.path.isdir(TURBOSHELL_USER_DIR):
        sys.path.append(TURBOSHELL_USER_DIR)

        if cmd_name == REBUILD_CMD:
            print(cmd_args)
        import scripts  # noqa

    if cmd_name in ts.commands:
        cmd = ts.commands[cmd_name]
        cmd(cmd_args)
    else:
        error('Turboshell could not find command "{}"'.format(cmd_name))


def print_help():
    print('Type turboshell.info for a list of commands.')


argv = sys.argv
if len(argv) == 1 or argv[1].lower().strip('-') in ('?', 'h', 'help'):
    print_help()
else:
    call_command(argv)
