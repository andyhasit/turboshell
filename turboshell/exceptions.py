

class CmdArgException(BaseException):
    """
    For when args are incorrectly specified in shell.
    """
    pass


class CmdDefinitionException(BaseException):
    """
    For issues with a command definition.
    """
    pass
