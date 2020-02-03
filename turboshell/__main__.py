"""
This module gets run when you call "python -m turboshell"
"""

import os
import sys
from .utils import error, TURBOSHELL_USER_DIR
from . import builtin_cmds  # noqa
from .collector import ac


def call_command(argv):
    """
    Calls a custom (user-defined) command.
    """
    try:
        name = argv[1]
        args = argv[2:]
    except IndexError:
        error('Use: "python -m turboshell cmd-name [...args]"')

    # These imports trigger the adding of aliases to the alias_collector
    import builtin_cmds  # noqa
    if TURBOSHELL_USER_DIR and os.path.isdir(TURBOSHELL_USER_DIR):
        sys.path.append(TURBOSHELL_USER_DIR)
        import scripts  # noqa

    if name in ac.commands:
        cmd = ac.commands[name]
        cmd(args)
    else:
        error('Turboshell could not find command "{}"'.format(name))


def print_help():
    print('Type turboshell.info for a list of commands.')


argv = sys.argv
if len(argv) == 1 or argv[1].lower().strip('-') in ('?', 'h', 'help'):
    print_help()
else:
    call_command(argv)
