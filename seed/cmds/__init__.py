"""
Use this file to control which modules are loaded.

1. Import local modules in this directory:

    from .examples import *
    # Remember to create __init__.py files in directories.

2. Import modules from turboshell.contrib:

    from turboshell.contrib.git import *

3. Import modules from other directory:

    sys.path.append('/some/other/directory')
    import your_cmds
    # Loads /some/other/directory/your_cmds.py
    # Note "your_cmds" could be a directory module too.

4. Import modules from distributed packages:

    from some_package import *
    # Note that "some_package" must be installed to the virtual environment
    # which turboshell runs in.

"""
from .playground import *
