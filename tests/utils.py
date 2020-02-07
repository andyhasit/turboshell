import shlex


def f(s):
    """Mimics shell arg splitting"""
    return shlex.split(s)
