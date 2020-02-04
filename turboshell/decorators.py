"""
Commands have parameters which will be passed as
"""
import re

# A regex for determining if a string is a POSIX options string like "-a" or "-abc"
OPT_REGEX = re.compile('^-{1}[\w]+$')

# Error messages 
TOO_FEW_ARGS = 'Expected at least {e} positional arguments but received {r}.'
TOO_MANY_ARGS = 'Expected at most {e} positional arguments but received {r}.'


class CmdArgException(BaseException):
    pass


def cmd(positional='', named='', alias=None, name=None):
    """
    A decorator which:
        - registers the function as a command
        - transforms the arguments passed to it from the terminal
    """
    def wrap(f):

        if name is None:  # noqa
            name = f.__name__

        def wrapped_f(shell_args):
            if requesting_help():
                print_help(f, positional, named, alias, name)
            else:
                try:
                    final_args = convert_args(shell_args, expected_positional, expected_named)
                    f(**processed_args)
                except CmdArgException as e:
                    print(e.message)
    
        # c.cmd(wrapped_f, alias=alias, name=name)
        # In case we inspect the function's name elsewhere...
        wrapped_f.__name__ = f.__name__
        return wrapped_f
    
    return wrap


def requesting_help(shell_args):
    """Determine whether user is asking for help"""
    for flag in ('?', '-h', '--help'):
        if flag in shell_args:
            return True
    return False


def print_help(f, positional, named, alias, name):
    """
    Print help information on command.
    """
    print('Help for turboshell command: {}'.format(name))
    print('Positional arguments: {}'.format(positional))
    print('Named arguments: {}'.format(named))
    print('Alias: {} (other aliases may be defined)'.format(alias))


def convert_args(shell_args, expected_positional=None, expected_named=None):
    """
    Converts the shell arguments into arguments for the function.
    """
    def clean_spec_str(str):
        if str is None:
            return []
        return str.split()

    expected_positional = clean_spec_str(expected_positional)
    expected_named = clean_spec_str(expected_named)

    options, received_positional, received_named = parse_shell_args(shell_args)
    min_arg_count = len([e for e in expected_positional if not e.endswith('?')])
    max_arg_count = len(expected_positional)
    received_arg_count = len(received_positional)

    # Check for too many positional args
    if received_arg_count > max_arg_count:
        raise CmdArgException(TOO_MANY_ARGS.format(
            e=max_arg_count, r=received_arg_count
        ))

    # Check for too few positional args
    if min_arg_count > received_arg_count:
        raise CmdArgException(TOO_FEW_ARGS.format(
            e=min_arg_count, r=received_arg_count
        ))


    # TODO: 
    #   only pass options if requested
    #   Process named args (can some be required?)


    final_args = {'options': options}

    # Process positional args using zip (ignores
    for r, e in zip(expected_positional, received_positional):
        name, value = extract_arg(r, e)
        final_args[name] = value


    return final_args


def extract_arg(value, definition):
    """
    Extracts the value and validates if appropriate
    """
    return value, definition
    #e.split(':')


def parse_shell_args(shell_args):
    options = []
    positional = []
    named = {}

    key = 'option_name'
    _save_as = {key: None}

    def save_as(name):
        if name and _save_as[key]:
            raise ValueError('Expected normal argument after {} but got {}'.format(_save_as[key], name))
        _save_as[key] = name

    if len(shell_args) > 0:

        # Determine if first chunk is like "-a" or "-abc"
        if OPT_REGEX.match(shell_args[0]):
            options = list(shell_args[0][1:])
            shell_args = shell_args[1:]
        
        # Process the remaining args
        for chunk in shell_args:
            if chunk.startswith('--'):
                # This indicates a flag e.g. "--verbose"
                options.append(chunk)
            elif chunk.startswith('-'):
                # This indicates a name argument e.g. "-name joe"
                save_as(chunk)
            else:
                # Normal string, so check if we're in save_as mode
                if _save_as[key]:
                    named[_save_as[key][1:]] = chunk
                else:
                    positional.append(chunk)
                save_as(None)

    return options, positional, named