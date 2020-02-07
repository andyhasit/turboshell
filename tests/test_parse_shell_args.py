import pytest
from turboshell.arg_utils import parse_shell_args, CmdArgException
from .utils import f


def test_allow_no_options():
    """
    Should not expect options section if has_options is false.
    """
    options, positional, named = parse_shell_args(f('-a hello'), has_options=False)
    assert options == []
    assert named == {'a': 'hello'}


def test_warn_if_no_value_provided():
    with pytest.raises(CmdArgException) as e:
        parse_shell_args(f('-a'), has_options=False)
    assert str(e.value) == 'Expected value after: -a'


def test_warn_if_named_arg_has_no_value():
    with pytest.raises(CmdArgException) as e:
        parse_shell_args(f('-a -b'), has_options=False)
    assert str(e.value) == 'Expected value after: -a'


def test_extracts_initial_options():
    options, positional, named = parse_shell_args(f('-a'), has_options=True)
    assert options == ['a']
    options, positional, named = parse_shell_args(f('-a -n jack'), has_options=True)
    assert options == ['a']
    options, positional, named = parse_shell_args(f('-abc -n jack'), has_options=True)
    assert options == ['a', 'b', 'c']


def test_extracts_extra_options():
    options, positional, named = parse_shell_args(f('xyz --my-opt'))
    assert options == ['my-opt']
    options, positional, named = parse_shell_args(f('-a --my-opt jack'), has_options=True)
    assert options == ['a', 'my-opt']
    options, positional, named = parse_shell_args(f('-a n jack --my-opt'), has_options=True)
    assert options == ['a', 'my-opt']


def test_handles_postitional_args():
    options, positional, named = parse_shell_args(f('-abc hello -n jack goodbye'), has_options=True)
    assert positional == ['hello', 'goodbye']
    options, positional, named = parse_shell_args(f('-abc hello goodbye'), has_options=True)
    assert positional == ['hello', 'goodbye']
    options, positional, named = parse_shell_args(f('-abc -n jack hello goodbye'), has_options=True)
    assert positional == ['hello', 'goodbye']
    options, positional, named = parse_shell_args(f('-abc hello goodbye -n jack'), has_options=True)
    assert positional == ['hello', 'goodbye']


def test_handles_named_args():
    options, positional, named = parse_shell_args(f('-abc -n jack'), has_options=True)
    assert named == {'n': 'jack'}
    options, positional, named = parse_shell_args(f('-abc hello -n jack'), has_options=True)
    assert named == {'n': 'jack'}
    options, positional, named = parse_shell_args(f('-abc -n jack goodbye'), has_options=True)
    assert named == {'n': 'jack'}
    options, positional, named = parse_shell_args(f('-abc hello -n jack goodbye'), has_options=True)
    assert named == {'n': 'jack'}
    options, positional, named = parse_shell_args(f('-abc a -n jack -a 23 b'), has_options=True)
    assert named == {'n': 'jack', 'a': '23'}
    options, positional, named = parse_shell_args(f('-abc -n jack xyz -a 23 b'), has_options=True)
    assert named == {'n': 'jack', 'a': '23'}
