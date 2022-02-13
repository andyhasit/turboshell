import os

TURBOSHELL_USER_DIR = os.environ.get('TURBOSHELL_USER_DIR')
TURBOSHELL_VENV_DIR = os.environ.get('TURBOSHELL_VENV_DIR')
TURBOSHELL_SHELL_DIR = os.path.join(TURBOSHELL_USER_DIR, 'shell')
USER_DEFINITIONS_FILE = os.path.join(TURBOSHELL_SHELL_DIR, 'definitions')
USER_INIT_FILE = os.path.join(TURBOSHELL_SHELL_DIR, 'init')
TURBOSHELL_EXEC = os.path.join(TURBOSHELL_SHELL_DIR, 'turboshell')
USER_MODULE_NAME = 'cmds'
REBUILD_CMD = "rebuild"
NO_CMD_MATCH = "---no-match---"
NO_SUBSHELL = "---no-subshell---"
CMD_SEP = "."


LIMIT_CMD_MATCH = int(os.environ.get('LIMIT_CMD_MATCH', 5))

# The name for the run last cmd alias (for command_not_found_handle)
RUN_LAST_FOUND_CMD = os.environ.get('TURBOSHELL_RUN_LAST_FOUND_CMD', 'u')

# Where the last cmd is stored (for command_not_found_handle)
LAST_FOUND_CMD_FILE="/tmp/turboshell_last_found"
