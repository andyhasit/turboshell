import os
import sys
import shutil
from turboshell.constants import REBUILD_CMD
from .file_generator import FileGenerator
from .utils import TURBOSHELL_USER_DIR, ensure_dir_exists
from .turboshell import ts


@ts.cmd()
def configure():
    """
    This command is called by user during installation, and whenever their turboshell directory moves.
    """
    target_dir = os.getcwd()
    this_dir = os.path.dirname(sys.argv[0])
    contrib_dir = os.path.join(os.path.dirname(this_dir), 'contrib')
    filegen = FileGenerator(target_dir)
    alias_file = filegen.definitions_file

    # Create turboshell script file
    filegen.generate_turboshell_script()

    # Copy files in contrib to user's scripts (doesn't overwrite if they exist)
    scripts_dir = os.path.join(target_dir, 'scripts')
    ensure_dir_exists(scripts_dir)
    for file in os.listdir(contrib_dir):
        source = os.path.join(contrib_dir, file)
        target = os.path.join(scripts_dir, file)
        if not os.path.exists(target):
            shutil.copy(source, target)

    # Ensure turboshell alias points to correct script
    # We don't want to overwrite their whole file, just redefine the alias in case it points to an old location
    if os.path.isfile(alias_file):
        with open(alias_file, 'a') as fp:
            fp.write("\n# These lines were added by configure command to ensure alias 'turboshell'\
                     points to the correct file.")
            fp.write('\n# They will be deleted on rebuild.')
            fp.write('\n{}\n'.format(filegen.turboshell_alias_line))
    else:
        filegen.generate_alias_file({}, {}, {}, {}, {})

    print("")
    print("  ---------------------------------")
    print("  TURBOSHELL SUCCESSFULLY INSTALLED")
    print("  ---------------------------------")
    print("\n  Add the following line to your shell initialisation file (e.g. ~/.bashrc or ~/.zshrc)")
    print("\n     source '{}'".format(alias_file))
    print("\n  This will load your aliases into new shell sessions.")
    print("  To load them into this shell session just run the above command at the prompt.")
    print("  You should then be able to run:")
    print("\n      turboshell.info")
    print("")


@ts.cmd(name=REBUILD_CMD)
def rebuild(*args):
    """
    Rebuilds the alias file.
    """
    filegen = FileGenerator(TURBOSHELL_USER_DIR)
    filegen.generate_alias_file(ts.aliases, ts.functions, ts.info_entries, ts.alias_groups, ts.group_info)
