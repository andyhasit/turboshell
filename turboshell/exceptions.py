

class CmdArgException(BaseException):
    """
    Exception to raise when args incorrectly specified in shell.
    """
    pass


class CmdSpecificationException(BaseException):
    """
    Exception to raise when args incorrectly specified by function.
    """
    pass
