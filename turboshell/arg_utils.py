"""
Commands have parameters which will be passed as
"""
import re
from .exceptions import CmdArgException
from .arg_specs import TextArgSpec
from .error_messages import (
    TOO_FEW_ARGS,
    TOO_MANY_ARGS, MISSING_NAMED_ARG,
    UNEXPECTED_NAMED_ARGS,
    UNEXPECTED_OPTION,
    EXPECTED_VALUE_AFTER_NAME
)

# A regex for determining if  swap to lists, oa string is a POSIX options string like "-a" or "-abc"
OPT_REGEX = re.compile('^-{1}[\w]+$')


def requesting_help(shell_args):
    """
    Determine whether user is invoking help.
    """
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


def convert_args(shell_args, expected_positional=None, expected_named=None, expected_options=None):
    """
    Converts the shell arguments into arguments for the function.
    May return None.
    """

    def convert_expected(arg_list):
        """
        Converts a list of arg_specs, some of which may be strings.
        """
        if arg_list is None:
            return []
        as_arg_specs = []
        for arg_spec in arg_list:
            if not hasattr(arg_spec, 'validate'):
                arg_spec = TextArgSpec(arg_spec)
            as_arg_specs.append(arg_spec)
        return as_arg_specs

    expected_positional = convert_expected(expected_positional)
    expected_named = convert_expected(expected_named)

    if expected_positional == [] and expected_named == [] and shell_args == []:
        return None

    has_options = expected_options is not None
    received_options, received_positional, received_named = parse_shell_args(shell_args, has_options)
    min_arg_count = len([e for e in expected_positional if e.required])
    max_arg_count = len(expected_positional)
    received_arg_count = len(received_positional)
    final_args = {}

    # Warn if too many positional args.
    if received_arg_count > max_arg_count:
        raise CmdArgException(TOO_MANY_ARGS.format(
            e=max_arg_count, r=received_arg_count
        ))

    # Warn if too few positional args.
    if min_arg_count > received_arg_count:
        raise CmdArgException(TOO_FEW_ARGS.format(
            e=min_arg_count, r=received_arg_count
        ))

    # Collect positional args.
    for arg_spec, value in zip(expected_positional, received_positional):
        arg_spec.validate(value)
        final_args[arg_spec.name] = arg_spec.value

    # Collect named args.
    for arg_spec in expected_named:
        name = arg_spec.name
        first_letter = name[0]
        for n in name, first_letter:
            if n in received_named:
                arg_spec.validate(received_named[n])
                final_args[name] = arg_spec.value
                del received_named[n]

    # Warn if required named args are unfulfilled.
    for arg_spec in expected_named:
        if not arg_spec.fulfilled():
            raise CmdArgException(MISSING_NAMED_ARG.format(arg_spec.name))

    # Warn if received unexpected named args.
    if len(received_named) > 0:
        raise CmdArgException(UNEXPECTED_NAMED_ARGS.format(', '.join(received_named.keys())))

    if expected_options:
        for k in received_options:
            print(k)
            if k not in expected_options:
                raise CmdArgException(UNEXPECTED_OPTION.format(k))

        final_args['options'] = received_options

    return final_args


def parse_shell_args(shell_args, has_options=False):
    """
    Returns options, positional, named
    e.g.
        cmd -as hello -n tommy --no-edit --include=*.py
    Returns (
            ['a', 's' , 'no-edit', 'include=*.py'],    # options
            ['hello'],                                 # positional
            {'n': 'tommy'}                             # named
            )
    """
    options = []
    positional = []
    named = {}

    key = 'option_name'
    _save_as = {key: None}

    def save_as(name):
        if name and _save_as[key]:
            raise CmdArgException(EXPECTED_VALUE_AFTER_NAME.format(_save_as[key]))
        _save_as[key] = name

    if len(shell_args) > 0:

        if has_options:
            # Determine if first chunk is like "-a" or "-abc"
            if OPT_REGEX.match(shell_args[0]):
                options = list(shell_args[0][1:])
                shell_args = shell_args[1:]

        # Process the remaining args
        for chunk in shell_args:
            if chunk.startswith('--'):
                # This indicates a flag e.g. "--verbose"
                options.append(chunk[2:])
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
        if _save_as[key]:
            raise CmdArgException(EXPECTED_VALUE_AFTER_NAME.format(_save_as[key]))

    return options, positional, named
