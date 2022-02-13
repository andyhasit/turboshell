import os
import sys
import shutil
from .builders import rebuild
from .turboshell import ts
from .ui import print_list
from .utils import is_empty, split_cmd_shortcut, write_to_file
from .vars import (
    CMD_SEP,
    REBUILD_CMD,
    FOUND_CMDS_FILE,
    LIMIT_CMD_MATCH,
    NO_CMD_MATCH,
    RUN_FOUND_CMD,
    TURBOSHELL_USER_DIR,
    TURBOSHELL_VENV_DIR,
    USER_INIT_FILE,
    NO_SUBSHELL
)


no_subshell = ["ts.rebuild", "ts.load"]


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
        'ts.list_dotted | turboshell match $*'
    )
    # "command_not_found_handle" is called by bash when a command is not found.
    # Here we check if the command has CMD_SEP, if so look for matches, and 
    # if we find exactly one match we run it.
    # "command_not_found_handle" runs in a sub-shell, so some things won't work.
    # We try to catch those and let the user run them in their shell.
    ts.func('command_not_found_handle',
        'if [[ $1 == *{}* ]] ; then'.format(CMD_SEP),
        '  CMD=$(ts.list_dotted | turboshell match $* | tee /dev/tty | tail -n 1)',
        '  if [[ $CMD == *{}* ]]; then'.format(NO_SUBSHELL),
        '    shift',
        '    CMD=$( cut -d " " -f 2- <<< "$CMD" )',
        '    echo "Turboshell won\'t run this command in a sub shell:"',
        '    echo "> $CMD $@"',
        '    echo Run it in the current shell with this command:',
        '    echo "> {}"'.format(RUN_FOUND_CMD),
        '  elif [ ! "$CMD" = "{}" ]; then'.format(NO_CMD_MATCH),
        '    shift',
        '    eval $CMD "$@"',
        '  fi',
        'fi',
        'echo Command not found',
        'return 127',
    )
    # Alias to run a found command
    ts.func(RUN_FOUND_CMD, 
        'N=$1',
        'eval $(tail -n+$N {} | head -n1)'.format(FOUND_CMDS_FILE)
        )


def _no_match():
    print(NO_CMD_MATCH)
    sys.exit(0)


def _dont_run_in_subshell(match):
    """
    Returns True if command should not be run in a subshell, because we want
    the effect to apply to the current shell. 
    So things like "cd" or "source" etc...
    """
    return match in no_subshell or match.startswith('cd.') or match.endswith('.cd')


@ts.cmd(name="match")
def match_command(*args):
    """
    Matches a command shortcut by splitting on "."
    If no command is found, the last line printed must be NO_CMD_MATCH.
    """
    try:
        if len(args) == 0:
            _no_match()
        cmd_chunks = split_cmd_shortcut(args[0])
        chunk_count = len(cmd_chunks)
        if chunk_count < 2:
            _no_match()
        matches = []
        for line in sys.stdin:
            line_chunks = line.split(CMD_SEP)
            if len(line_chunks) < chunk_count:
                continue
            chunk_match = 0
            for cmd_chunk, line_chunk in zip(cmd_chunks, line_chunks):
                if not line_chunk.startswith(cmd_chunk):
                    continue
                chunk_match += 1
            if chunk_match == chunk_count:
                matches.append(line.strip())
        write_to_file(FOUND_CMDS_FILE, matches[:LIMIT_CMD_MATCH])
        match_count = len(matches)
        if match_count == 1:
            match = matches[0]
            if _dont_run_in_subshell(match):
                print(NO_SUBSHELL, match)
            else:
                print(match)
            sys.exit(0)
        elif match_count > 1:
            print("Turboshell found multiple matches:")
            print()
            print_list(matches, 1, LIMIT_CMD_MATCH)
            print()
            if match_count > LIMIT_CMD_MATCH:
                print(f"Found {match_count - LIMIT_CMD_MATCH} more matches not shown.")
                print()
            print("Run your choice with cmd 'u' followed by the number, e.g.")
            print("> u 1")
            _no_match()
    except Exception as e:
        print(e)
        _no_match()


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


if ts.is_collecting:
    generate_builtins()
