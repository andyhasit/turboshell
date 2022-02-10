from .vars import USER_DEFINITIONS_FILE, REBUILD_CMD
from .loaders import load_user_cmds
from .turboshell import ts
from .utils import error
from .writer import Writer


@ts.cmd(name=REBUILD_CMD, args=["module", "target"], info="Rebuilds a definitions file")
def rebuild(module=None, target=None):
    """
    Rebuilds the target definitions file from the module.
    If both are None, uses the default user module and definitions file.
    """
    ts.is_collecting = True
    if module is None and target is None:
        ts.settings.set(include_builtins=True)
        load_user_cmds()
        target = USER_DEFINITIONS_FILE
    elif module and target:
        ts.settings.set(include_builtins=False)
        try:
            __import__(module)
        except ModuleNotFoundError as err:
            error(f"{err} - you specify a module available from the current working directory (e.g. foo.bar)")
    else:
        error('Must supply both arguments "module" and "target" or neither.')
    
    writer = Writer(ts, target)
    writer.write()