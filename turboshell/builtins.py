import os
import sys
import shutil
from .rebuild import rebuild
from .turboshell import ts
from .utils import is_empty, split_cmd_shortcut
from .vars import (
    TURBOSHELL_VENV_DIR,
    USER_DEFINITIONS_FILE,
    REBUILD_CMD,
    NO_CMD_MATCH,
    CMD_SEP
)


def generate_builtins():
    turboshell_func_lines = ["python -m turboshell $*"]

    if not is_empty(TURBOSHELL_VENV_DIR):

        ts.alias("ts.venv.activate", f"source '{TURBOSHELL_VENV_DIR}/bin/activate'")

        turboshell_func_lines.insert(0, "ts.venv.activate")

    ts.func("turboshell", *turboshell_func_lines)

    ts.alias("ts.reload", f"source {USER_DEFINITIONS_FILE}")
    ts.func("ts.rebuild", 
        f"turboshell {REBUILD_CMD} $*",
        "ts.reload"
    )
    ts.alias("ts.help", f"echo coming!!!")
    ts.func('ts.list_dotted',
        'cat <(alias | cut -d= -f1 | cut -d\' \' -f2 | grep "\.") <(declare -F | cut -d \' \' -f3 | grep "\.")'
    )
    ts.func('ts.find',
        'ts.list_dotted | turboshell find $* | tee /dev/tty | tail -n 1'
    )
    # https://www.linuxjournal.com/content/bash-command-not-found
    # https://stackoverflow.com/questions/5370260/how-to-change-current-working-directory-inside-command-not-found-handle
    # TODO: maybe use stderr to avoid print out?
    ts.func('command_not_found_handle',
        #'shopt -s autocd',
        'CMD=$(ts.list_dotted | turboshell find $* | tee /dev/tty | tail -n 1)',
        # f'if [[ $CMD = cd* ]]; then',
        # 'echo 888',
        # ' echo "${CMD:2:*}"',
        # ' echo "${CMD#*cd.}"',
        'cd /other',
        f'if [ ! "$CMD" = "{NO_CMD_MATCH}" ]; then',
        '  eval "$CMD"',
        'else',
        '  return 127',
        'fi',
    )


if ts.is_collecting:
    generate_builtins()


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


@ts.cmd(name="find")
def find_command(*args):
    """
    Finds a command shortcut by splitting on "."
    """
    if len(args) == 0:
        return
    cmd_chunks = split_cmd_shortcut(args[0])
    chunk_count = len(cmd_chunks)
    if chunk_count < 2:
        return
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
    elif len(matches) > 1:
        print("Turboshell found multiple matches:")
        print()
        for match in matches:
            print(' ', match)
        print()
        print(NO_CMD_MATCH)
