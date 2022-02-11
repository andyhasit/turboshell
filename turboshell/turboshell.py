import os
from .arg_utils import convert_args, print_help, requesting_help
from .exceptions import CmdArgException, CmdSpecificationException
from .utils import get_full_name
from .settings import Settings


class Turboshell:

    def __init__(self):
        self.is_collecting = False
        self.settings = Settings()
        self.aliases = {}
        self.functions = {}
        self.commands = {}
        self.info_entries = {}
        self.group_info = {}
        self.alias_groups = {}

    def set(self, **kwargs):
        self.settings.set(**kwargs)

    def cmd(self, alias=None, arg=None, args=None, kwargs=None, name=None, info=None, group=None):
        """
        A decorator which:
            - registers the function as a command
            - transforms the shell args passed to the function
        """
        # TODO: use functools
        def wrap(func):

            # Be careful not to assign over name as that makes it a local variable
            cmd_name = name or get_full_name(func)

            def wrapped_f(shell_args):
                """
                This is the function which finally gets executed.
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
                    except CmdSpecificationException as e:
                        print('Error with command definition')
                        print(e)

            self.command(wrapped_f, cmd_name, alias=alias, info=info, group=group)

            # In case we inspect the function's name elsewhere...
            wrapped_f.__name__ = func.__name__

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
            raise CmdSpecificationException('Command with name "{}" already exists'.format(name))
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
        clean_lines = [line.strip() for line in clean_lines]
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


# This is a global object to which all modules add their aliases
ts = Turboshell()
