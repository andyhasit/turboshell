import os
import sys
import shutil
from .vars import TURBOSHELL_VENV_DIR, USER_DEFINITIONS_FILE, TURBOSHELL_USER_DIR, REBUILD_CMD
from .utils import is_empty, ensure_dir_exists
from .turboshell import ts


if ts.is_collecting:
    
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


@ts.cmd(name='init')
def init():
    """
    Creates inital files in current directory
    """
    target_dir = os.getcwd()
    this_dir = os.path.dirname(sys.argv[0])
    contrib_dir = os.path.join(os.path.dirname(this_dir), 'contrib')
    

    #filegen = FileGenerator(target_dir)
    #alias_file = filegen.definitions_file

    # Copy files in contrib to user's scripts (doesn't overwrite if they exist)
    ensure_dir_exists(scripts_dir)
    for file in os.listdir(contrib_dir):
        source = os.path.join(contrib_dir, file)
        target = os.path.join(TURBOSHELL_USER_DIR, file)
        #os.makedirs(os.path.dirname(filePath), exist_ok=True)
        if not os.path.exists(target):
            shutil.copy(source, target)

    # Ensure turboshell alias points to correct script
    # We don't want to overwrite their whole file, just redefine the alias in case it points to an old location
    # if os.path.isfile(alias_file):
    #     with open(alias_file, 'a') as fp:
    #         fp.write("\n# These lines were added by configure command to ensure alias 'turboshell'\
    #                  points to the correct file.")
    #         fp.write('\n# They will be deleted on rebuild.')
    #         fp.write('\n{}\n'.format(filegen.turboshell_alias_line))
    # else:
    #     filegen.generate_alias_file({}, {}, {}, {}, {})

    #filegen.generate_alias_file({}, {}, {}, {}, {})
    filegen.generate_alias_file(ts.aliases, ts.functions, ts.info_entries, ts.alias_groups, ts.group_info)

    print("Files generated")

    # print("  ---------------------------------")
    # print("  TURBOSHELL SUCCESSFULLY INSTALLED")
    # print("  ---------------------------------")
    # print("\n  Add the following line to your shell initialisation file (e.g. ~/.bashrc or ~/.zshrc)")
    # print("\n     source '{}'".format(alias_file))
    # print("\n  This will load your aliases into new shell sessions.")
    # print("  To load them into this shell session just run the above command at the prompt.")
    # print("  You should then be able to run:")
    # print("\n      turboshell.info")
    # print("")

