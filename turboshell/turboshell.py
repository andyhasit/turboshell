from collections import defaultdict
from .arg_utils import convert_args, print_help, requesting_help
from .exceptions import CmdArgException, CmdSpecificationException


class TurboshellSingleton:

    def __init__(self):
        self.aliases = {}
        self.functions = {}
        self.commands = {}
        self.info_entries = {}
        self.group_info = {}
        self.alias_groups = {}

    def cmd(self, alias=None, args=None, kwargs=None, name=None, options=None, info=None, group=None):
        """
        A decorator which:
            - registers the function as a command
            - transforms the shell args passed to the function
        """
        def wrap(original_function):

            # Be careful not to assign over name as that makes it a local variable
            cmd_name = name or original_function.__name__

            def wrapped_f(shell_args):
                if requesting_help(shell_args):
                    print_help(original_function, args, kwargs, alias, cmd_name)
                else:
                    try:
                        final_args = convert_args(shell_args, args, kwargs)
                        if final_args:
                            original_function(**final_args)
                        else:
                            original_function()
                    except CmdArgException as e:
                        print(e)
                    except CmdSpecificationException as e:
                        print('Error with command definition')
                        print(e)

            self.command(wrapped_f, cmd_name, alias=alias, info=info, group=group)

            # In case we inspect the function's name elsewhere...
            wrapped_f.__name__ = original_function.__name__

            return wrapped_f

        return wrap

    def command(self, function, name, alias=None, info=None, group=None):
        """
        Registers a command as "turboshell [name]" where name is the name of the function.
        @name if provided, sets the name of the command, else name of function is used.
        @alias creates an alias for the command.
        @info is only used if alias is also provided.
        """
        self.commands[name] = function
        if alias:
            self.alias(alias, 'turboshell ' + name)
            if info:
                self.info(alias, info, group)

    def alias(self, name, command, info=None, group=None):
        """Add a single alias"""
        self.aliases[name] = command
        if info:
            self.info(name, info, group)

    def aliases(self, items):
        """Add a list of aliases"""
        for entry in items:
            self.alias(*entry)

    def func(self, name, lines, info=None, group=None):
        """Add a single function"""
        self.functions[name] = lines
        if info:
            self.info(name, info, group)

    def info(self, alias, text, group=None):
        """Add an entry for the info command"""
        if group:
            self.alias_groups[alias] = group
        self.info_entries[alias] = text


# This is a global object to which all modules add their aliases
ts = TurboshellSingleton()
