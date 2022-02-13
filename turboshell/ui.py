
def print_list(items, start=None, stop=None):
    """
    Prints a list, optionally numbered.
    """
    for i, item in enumerate(items, 0):
        if stop and (i + 1) > stop:
            break
        if start is not None:
            number = start + i
            space = 3 - len(str(number))
            pad = " " * space
            print(f"  {pad}{number} - {item}")
        else:
            print(f"  {item}")