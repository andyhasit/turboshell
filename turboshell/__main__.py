"""
This module gets run when you call "python -m turboshell"
"""

import os
import sys
from .utils import error
from .env_vars import TURBOSHELL_USER_DIR
from .file_generator import FileGenerator
from .turboshell import ts
from .constants import REBUILD_CMD


@ts.cmd(name="build", args=["module", "out"])
def build(module, out):
    """
    Rebuilds an alias file.
    """
    print(999)
    # filegen = FileGenerator(TURBOSHELL_USER_DIR)
    # filegen.generate_alias_file(ts.aliases, ts.functions, ts.info_entries, ts.alias_groups, ts.group_info)


@ts.cmd(name=REBUILD_CMD)
def rebuild(*args):
    """
    Rebuilds the user alias file.
    """
    filegen = FileGenerator(TURBOSHELL_USER_DIR)
    filegen.generate_alias_file(ts.aliases, ts.functions, ts.info_entries, ts.alias_groups, ts.group_info)


def call_command(argv):
    """
    Calls a custom (user-defined) command.
    """
    try:
        cmd_name = argv[1]
        cmd_args = argv[2:]
    except IndexError:
        error('Use: "python -m turboshell cmd-name [...args]"')
    
    # These are special cases 
    if cmd_name in ["build", "rebuild"]:
        cmd = ts.commands[cmd_name]
        cmd(cmd_args)
        return

    from . import builtin_cmds  # noqa
    if cmd_name not in ts.commands:
        if TURBOSHELL_USER_DIR and os.path.isdir(TURBOSHELL_USER_DIR):
            sys.path.append(TURBOSHELL_USER_DIR)
            import scripts  # noqa

    if cmd_name in ts.commands:
        cmd = ts.commands[cmd_name]
        cmd(cmd_args)
    else:
        error('Could not find Turboshell command "{}"'.format(cmd_name))


def print_instructions():
    print('Type turboshell.info for a list of commands.')


argv = sys.argv
if len(argv) == 1 or argv[1].lower().strip('-') in ('?', 'h', 'help'):
    print_instructions()
else:
    call_command(argv)
