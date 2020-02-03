
class AliasCollector:

    def __init__(self):
        self.aliases = {}
        self.functions = {}
        self.commands = {}
        self.info_entries = []

    def cmd(self, function, alias=None, info=None, name=None):
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

    def add_many(self, items):
        """Add a list of aliases"""
        for name, command in items:
            self.alias(name, command)

    def function(self, name, lines, info=None):
        """Add a single function"""
        self.functions[name] = lines
        if info:
            self.info(name, info)

    def info(self, title, text):
        """Add an entry for the info command"""
        self.info_entries.append((title, text))


# This is a global object to which all modules add their aliases
ac = AliasCollector()
