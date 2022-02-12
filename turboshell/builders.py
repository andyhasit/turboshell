from .vars import USER_RC_FILE, REBUILD_CMD
from .loaders import load_user_cmds
from .turboshell import ts
from .utils import error
from .writer import Writer


@ts.cmd(name=REBUILD_CMD)
def rebuild():
    """
    Reuilds the user definitions file from the user cmds module.
    """
    ts.is_collecting = True
    ts.settings.set(include_builtins=True)
    load_user_cmds()
    target = USER_RC_FILE
    writer = Writer(ts, target)
    writer.write()


@ts.cmd(name="build", args=["module", "target"])
def build(module=None, target=None):
    """
    Builds the target definitions file from the module.
    """
    ts.is_collecting = True
    ts.settings.set(include_builtins=False)
    try:
        __import__(module)
    except ModuleNotFoundError as err:
        error(f"{err} - specify a module name (e.g. foo.bar)")
    writer = Writer(ts, target)
    writer.write()