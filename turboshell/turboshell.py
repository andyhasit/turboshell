import os
import functools
from .arg_utils import convert_args, print_help, requesting_help
from .exceptions import CmdArgException, CmdDefinitionException
from .utils import get_full_name
from .settings import Settings
from . import ui
from . import shell


class Turboshell:
    """
    The main object accessed by user code.
    Exposes methods for adding definitions, and access to other apis
    """

    def __init__(self):
        self.args = ()
        self.collecting = False
        self.settings = Settings()
        self.aliases = {}
        self.functions = {}
        self.commands = {}
        self.info_entries = {}
        self.group_info = {}
        self.alias_groups = {}
        self.vars = {}
        self.ui = ui
        self.shell = shell

    def var(self, name, func):
        cmd_name = get_full_name(func)
        self.cmd(name=cmd_name)(func)
        return f"{name}=$(turboshell {cmd_name} $*)"
        
    def set(self, **kwargs):
        self.settings.set(**kwargs)

    def cmd(self, alias=None, arg=None, args=None, kwargs=None, name=None, info=None, group=None):
        """
        A decorator which:
            - registers the function as a command
            - transforms the shell args passed to the function
        """

        def wrap(func):
            
            cmd_name = name or get_full_name(func)

            @functools.wraps(func)
            def wrapped_f(shell_args):
                """
                This function parses the shell_args and calls the command's function.
                """
                if requesting_help(shell_args):
                    print_help(func, args, kwargs, alias, cmd_name)
                else:
                    try:
                        if arg:
                            func(" ".join(shell_args))
                        elif args or kwargs:
                            final_args = convert_args(shell_args, args, kwargs)
                            func(**final_args)
                        else:
                            func(*shell_args)
                    except CmdArgException as e:
                        print(e)
                    except CmdDefinitionException as e:
                        print('Error with command definition')
                        print(e)

            self.command(wrapped_f, cmd_name, alias=alias, info=info, group=group)
            return wrapped_f

        return wrap

    def command(self, function, name, alias=None, info=None, group=None):
        """
        Registers a command as "turboshell [name]" where name is the name of the function.
        @name if provided, sets the name of the command, else name of function is used.
        @alias creates an alias for the command.
        @info is only used if alias is also provided.
        """
        if name in self.commands:
            raise CmdDefinitionException('Command with name "{}" already exists'.format(name))
        self.commands[name] = function
        if alias:
            self.alias(alias, 'turboshell ' + name)
            if info:
                self.info(alias, info, group)

    def alias(self, name, command, info=None, group=None):
        """
        Add a single alias.
        """
        self.aliases[name] = command
        if info:
            self.info(name, info, group)

    def aliases(self, items):
        """
        Add a list of aliases.
        """
        for entry in items:
            self.alias(*entry)

    def func(self, name, *lines, info=None, group=None):
        """
        Add a single function.
        """
        clean_lines = []
        for line in lines:
            clean_lines.extend(line.split(os.linesep))
        clean_lines = [line.rstrip() for line in clean_lines]
        clean_lines = [line for line in clean_lines if line != ""]
        self.functions[name] = clean_lines
        if info:
            self.info(name, info, group)

    def info(self, alias, text, group=None):
        """
        Add an entry for the info command.
        """
        if group:
            self.alias_groups[alias] = group
        self.info_entries[alias] = text

    def group(self, name, lines):
        """
        Create a group for grouping info lines.
        """
        self.group_info[name] = lines

    def group(self, name, value):
        """
        Define a variable
        """
        self.vars[name] = value


# This is a global object to which all modules add their aliases
ts = Turboshell()
