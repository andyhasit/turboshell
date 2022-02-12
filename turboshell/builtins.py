import os
import sys
import shutil
from .rebuild import rebuild
from .turboshell import ts
from .utils import is_empty, split_cmd_shortcut
from .vars import (
    CMD_SEP,
    REBUILD_CMD,
    LAST_FOUND_CMD_FILE,
    NO_CMD_MATCH,
    RUN_LAST_FOUND_CMD,
    TURBOSHELL_VENV_DIR,
    USER_DEFINITIONS_FILE,
)


def generate_builtins():
    """
    Include all builtins here, we can pop keys later according to settings.
    """

    ts.func("ts.rebuild", f"turboshell {REBUILD_CMD} $*", "ts.load", 
        info="Rebuilds the alias file and loads it.")
    ts.alias("ts.load", f"source {USER_DEFINITIONS_FILE}")
    ts.alias("ts.help", f"ts.info")

    if not is_empty(TURBOSHELL_VENV_DIR):
        ts.alias("ts.venv.activate", f"source '{TURBOSHELL_VENV_DIR}/bin/activate'")

    # Echos all aliases and functions with CMD_SEP
    ts.func('ts.list_dotted',
        f'cat <(alias | cut -d= -f1 | cut -d\' \' -f2 | grep "\{CMD_SEP}")\
              <(declare -F | cut -d \' \' -f3 | grep "\{CMD_SEP}")'
    )
    # A way to check what the command matcher will return
    ts.func('ts.match',
        'ts.list_dotted | turboshell find $*'
    )
    # "command_not_found_handle" is called by bash when a command is not found.
    # Here we check if the command has CMD_SEP, if so look for matches, and 
    # if we find exactly one match we run it.
    # "command_not_found_handle" runs in a sub-shell, so cd won't work. 
    # But we copy the command to a temp file and let the user recall it with
    # the alias "u".
    ts.func('command_not_found_handle',
        'if [[ $1 == *{}* ]] ; then'.format(CMD_SEP),
        '  CMD=$(ts.list_dotted | turboshell find $* | tee /dev/tty | tail -n 1)',
        '  if [ ! "$CMD" = "{}" ]; then'.format(NO_CMD_MATCH),
        '    shift',
        '    echo $CMD "$@" > {}'.format(LAST_FOUND_CMD_FILE),
        '    eval $CMD "$@"',
        '  fi',
        'fi',
        'return 127',
    )
    # Alias to run what is in LAST_FOUND_CMD_FILE
    ts.alias(RUN_LAST_FOUND_CMD, f'eval $(cat {LAST_FOUND_CMD_FILE})')


def _no_match():
    print(NO_CMD_MATCH)
    sys.exit(0)


@ts.cmd(name="find")
def find_command(*args):
    """
    Finds a command shortcut by splitting on "."
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
        if len(matches) == 1:
            print(matches[0])
            sys.exit(0)
        elif len(matches) > 1:
            print("Turboshell found multiple matches:")
            print()
            for match in matches:
                print(' ', match)
            print()
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
    contrib_dir = os.path.join(os.path.dirname(this_dir), 'contrib')

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
