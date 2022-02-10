import os
import sys
from .utils import error
from .vars import TURBOSHELL_USER_DIR


def load_user_cmds():
    if TURBOSHELL_USER_DIR and os.path.isdir(TURBOSHELL_USER_DIR):
        sys.path.append(TURBOSHELL_USER_DIR)
        try:
            import cmds  # noqa
        except ModuleNotFoundError:
            error(f'Expected to find Python module "cmds" in {TURBOSHELL_USER_DIR}')
    else:
        error(f'Could not find directory {TURBOSHELL_USER_DIR}')


def load_builtin_cmds():
    from . import builtins  # noqa
