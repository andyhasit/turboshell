import os
import sys
from .utils import error
from .vars import TURBOSHELL_USER_DIR


def load_user_cmds():
    """
    Loads commands from user's cmds module.
    """
    if TURBOSHELL_USER_DIR and os.path.isdir(TURBOSHELL_USER_DIR):
        sys.path.append(TURBOSHELL_USER_DIR)
        try:
            import cmds  # noqa
        except ModuleNotFoundError as err:
            error(f'Error importing {err} path: {sys.path}')
    else:
        error(f'Could not find directory {TURBOSHELL_USER_DIR}')


def load_builtin_cmds():
    from . import builtins  # noqa


def load_builder_cmds():
    from . import builders  # noqa
