import pytest
import shlex
from turboshell.decorators import CmdArgException, convert_args, parse_shell_args


def f(s):
    """Mimics shell arg splitting"""
    return shlex.split(s)


def test_parse_shell_args_extracts_initial_options():
    options, positional, named = parse_shell_args(f('-a'))
    assert options == ['a']
    options, positional, named = parse_shell_args(f('-a -n jack'))
    assert options == ['a']
    options, positional, named = parse_shell_args(f('-abc -n jack'))
    assert options == ['a', 'b', 'c']


def test_parse_shell_args_extracts_extra_options():
    options, positional, named = parse_shell_args(f('xyz --my-opt'))
    assert options == ['--my-opt']
    options, positional, named = parse_shell_args(f('-a --my-opt jack'))
    assert options == ['a', '--my-opt']
    options, positional, named = parse_shell_args(f('-a n jack --my-opt'))
    assert options == ['a', '--my-opt']


def test_parse_shell_args_handles_postitional_args():
    options, positional, named = parse_shell_args(f('-abc hello -n jack goodbye'))
    assert positional == ['hello', 'goodbye']
    options, positional, named = parse_shell_args(f('-abc hello goodbye'))
    assert positional == ['hello', 'goodbye']
    options, positional, named = parse_shell_args(f('-abc -n jack hello goodbye'))
    assert positional == ['hello', 'goodbye']
    options, positional, named = parse_shell_args(f('-abc hello goodbye -n jack'))
    assert positional == ['hello', 'goodbye']


def test_parse_shell_args_handles_named_args():
    options, positional, named = parse_shell_args(f('-abc -n jack'))
    assert named == {'n': 'jack'}
    options, positional, named = parse_shell_args(f('-abc hello -n jack'))
    assert named == {'n': 'jack'}
    options, positional, named = parse_shell_args(f('-abc -n jack goodbye'))
    assert named == {'n': 'jack'}
    options, positional, named = parse_shell_args(f('-abc hello -n jack goodbye'))
    assert named == {'n': 'jack'}
    options, positional, named = parse_shell_args(f('-abc a -n jack -a 23 b'))
    assert named == {'n': 'jack', 'a': '23'}
    options, positional, named = parse_shell_args(f('-abc -n jack xyz -a 23 b'))
    assert named == {'n': 'jack', 'a': '23'}


def test_convert_args_handles_positionals():
    expected_positional = 'name age'
    expected_named = ''

    with pytest.raises(CmdArgException):
        final_args = convert_args(f('jack'), expected_positional)

    with pytest.raises(CmdArgException):
        final_args = convert_args(f('jack 23 unexpected-arg'), expected_positional)

    final_args = convert_args(f('jack 23'), expected_positional)
    assert final_args == {'name': 'jack', 'age': '23', 'options': []}
