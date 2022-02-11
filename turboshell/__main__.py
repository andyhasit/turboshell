"""
The module which runs when you call "python -m turboshell"
"""
import sys
from .loaders import load_builtin_cmds, load_user_cmds
from .turboshell import ts
from .utils import error, print_instructions
from .rebuild import rebuild


def call_command(argv):
    """
    Calls a command, which could be builtin or user-defined.
    """
    try:
        cmd_name = argv[1]
        cmd_args = argv[2:]
    except IndexError:
        error('You must provide a command name')
    
    if cmd_name == "rebuild":
        rebuild(cmd_args)
        return
    
    load_builtin_cmds()
    if cmd_name not in ts.commands:
        load_user_cmds()
    if cmd_name in ts.commands:
        cmd = ts.commands[cmd_name]
        cmd(cmd_args)
    else:
        error('Could not find Turboshell command "{}"'.format(cmd_name))


if __name__ == "__main__":
    argv = sys.argv
    if len(argv) == 1 or argv[1].lower().strip('-') in ('?', 'h', 'help'):
        print_instructions()
    else:
        call_command(argv)
