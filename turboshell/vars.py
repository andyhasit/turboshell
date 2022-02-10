import os

TURBOSHELL_USER_DIR = os.environ.get('TURBOSHELL_USER_DIR')
TURBOSHELL_VENV_DIR = os.environ.get('TURBOSHELL_VENV_DIR')

USER_DEFINITIONS_FILE = os.path.join(TURBOSHELL_USER_DIR, 'build', 'definitions')

USER_MODULE_NAME = 'cmds'
REBUILD_CMD = "rebuild"