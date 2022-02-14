
def print_list(items, start=None, stop=None, out=None):
    """
    Prints a list, optionally numbered.
    """
    if out is None:
        out = print
    for i, item in enumerate(items, 0):
        if stop and (i + 1) > stop:
            break
        if start is not None:
            number = start + i
            space = 3 - len(str(number))
            pad = " " * space
            out(f"  {pad}{number} - {item}")
        else:
            out(f"  {item}")