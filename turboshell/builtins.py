import os
import sys
import shutil
from .builders import rebuild
from .matcher import find_matching_commands
from .turboshell import ts
from .utils import error, is_empty, split_cmd_shortcut, write_to_file
from .vars import (
    CMD_SEP,
    REBUILD_CMD,
    FOUND_CMDS_FILE,
    LIMIT_CMD_MATCH,
    RUN_FOUND_CMD,
    TURBOSHELL_USER_DIR,
    TURBOSHELL_VENV_DIR,
    USER_INIT_FILE,
)


def generate_builtins():
    """
    Include all builtins here, we can pop keys later according to settings.
    """

    ts.func("ts.rebuild", f"turboshell {REBUILD_CMD} $*", "ts.load", 
        info="Rebuilds the user definitions from cmds and loads them.")
    ts.alias("ts.load", f"source {USER_INIT_FILE}")
    ts.alias("ts.help", f"ts.info")
    ts.alias("ts.home", f'cd "{TURBOSHELL_USER_DIR}"')

    if not is_empty(TURBOSHELL_VENV_DIR):
        ts.alias("ts.venv.activate", f"source '{TURBOSHELL_VENV_DIR}/bin/activate'")

    # Echos all aliases and functions with CMD_SEP
    ts.func('ts.list_dotted',
        f'cat <(alias | cut -d= -f1 | cut -d\' \' -f2 | grep "\{CMD_SEP}")\
              <(declare -F | cut -d \' \' -f3 | grep "\{CMD_SEP}")'
    )
    # A way to check what the command matcher will return
    ts.func('ts.match',
        'ts.list_dotted | turboshell find_match_info $*'
    )

    # "command_not_found_handle" is called by bash when a command is not found.
    # Here we check if the command has CMD_SEP, if so look for matches, and 
    # if we find exactly one match we run it.
    # "command_not_found_handle" runs in a sub-shell, so some things won't work.
    # We try to catch those and let the user run them in their shell.

    ts.func('command_not_found_handle',
        'if [[ $1 == *{}* ]] ; then'.format(CMD_SEP),
        '  CMD=$(ts.list_dotted | turboshell find_match_exec $* | tee /dev/tty | tail -n 1)',
        '  if [[ ! -z $CMD ]]; then',
        '    if [[ ! $CMD =~ " " ]]; then'
        '      shift',
        '      eval $CMD "$@"',
        '    fi',
        '  else',
        '    echo Command not found',
        '    return 127',
        '  fi',
        'else',
        '  echo Command not found',
        '  return 127',
        'fi',
    )
    # Alias to run a found command
    ts.func(RUN_FOUND_CMD, 
        'if [[ $1 ]] ; then',
        '  N=$1',
        'else'
        '  N=1',
        'fi',
        'CMD=$(tail -n+$N {} | head -n1)'.format(FOUND_CMDS_FILE),
        '> {}'.format(FOUND_CMDS_FILE),
        'if [[ ! -z $CMD ]]; then',
        '  eval $CMD',
        'else',
        '  echo You can only enter numbers after Turboshell matching.',
        'fi'
        )
    for i in range(1, LIMIT_CMD_MATCH):
        ts.alias(f'{i}', f'{RUN_FOUND_CMD} {i}')


@ts.cmd(name="find_match_exec")
def find_match_exec(*args):
    """
    Matches a command shortcut by splitting on "."

    WARNING:

    This function is called by "command_not_found_handle" which inspects the
    last line of output, and will run it with "eval" if it contains no spaces.

    It's a bit of a hack, which we might be able to get rid of with STDERR or
    something.

    Until then, ensure the last line of output definitely contains spaces if 
    we did not find exactly one match, and it should run.
    """
    space = " "
    try:
        matches, output, run = find_matching_commands(args, sys.stdin, True)
        if len(matches) != 1 or not run:
            last_line = output[-1]
            assert space in last_line
        for line in output:
            print(line)
    except Exception as err:
        print(err)
        print("Internal error")
    return


@ts.cmd(name="find_match_info")
def find_match_exec(*args):
    matches, output, run = find_matching_commands(args, sys.stdin, False)
    for line in output:
        print(line)


@ts.cmd(name='init')
def init():
    """
    Creates inital files in current directory.
    """
    target_dir = os.getcwd()
    this_dir = os.path.dirname(sys.argv[0])
    contrib_dir = os.path.join(os.path.dirname(this_dir), 'seed')

    for root, dirs, files in os.walk(contrib_dir):
        for d in dirs:
            source = os.path.join(root, d)
            target = source.replace(contrib_dir, target_dir)
            os.makedirs(target, exist_ok=True)
        for file in files:
            source = os.path.join(root, file)
            target = source.replace(contrib_dir, target_dir)
            if not os.path.exists(target):
                shutil.copy(source, target)
                print(f"Created: {target}")
    generate_builtins()
    rebuild(())


if ts.collecting:
    generate_builtins()
