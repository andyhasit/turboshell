from .arg_utils import convert_args, print_help, requesting_help
from .exceptions import CmdArgException, CmdSpecificationException


class TurboshellSingleton:

    def __init__(self):
        self.aliases = {}
        self.functions = {}
        self.commands = {}
        self.info_entries = []

    def cmd(self, alias=None, positional=None, named=None, name=None, options=None):
        """
        A decorator which:
            - registers the function as a command
            - transforms the shell args passed to the function
        """
        def wrap(f):

            def wrapped_f(shell_args):
                # Be careful not to assign over name as that makes it a local variable
                cmd_name = name or f.__name__
                if requesting_help(shell_args):
                    print_help(f, positional, named, alias, cmd_name)
                else:
                    try:
                        final_args = convert_args(shell_args, positional, named)
                        if final_args:
                            f(**final_args)
                        else:
                            f()
                    except (CmdArgException, CmdSpecificationException) as e:
                        print(e.info)

            self.command(wrapped_f, alias=alias, name=name)

            # In case we inspect the function's name elsewhere...
            wrapped_f.__name__ = f.__name__

            return wrapped_f

        return wrap

    def command(self, function, alias=None, info=None, name=None):
        """
        Registers a command as "turboshell [name]" where name is the name of the function.
        @name if provided, sets the name of the command, else name of function is used.
        @alias creates an alias for the command.
        @info is only used if alias is also provided.
        """
        if name is None:
            name = function.__name__
        self.commands[name] = function
        if alias:
            self.alias(alias, 'turboshell ' + name)
            if info:
                self.info(alias, info)

    def alias(self, name, command, info=None):
        """Add a single alias"""
        self.aliases[name] = command
        if info:
            self.info(name, info)

    def aliases(self, items):
        """Add a list of aliases"""
        for entry in items:
            self.alias(*entry)

    def func(self, name, lines, info=None):
        """Add a single function"""
        self.functions[name] = lines
        if info:
            self.info(name, info)

    def info(self, title, text):
        """Add an entry for the info command"""
        self.info_entries.append((title, text))


# This is a global object to which all modules add their aliases
ts = TurboshellSingleton()
