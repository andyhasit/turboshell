import pytest
from turboshell.arg_utils import convert_args, CmdArgException
from .utils import f


def test_convert_args_fails_with_too_many_positionals():
    expected_positional = ['name!', 'age!']
    with pytest.raises(CmdArgException):
        convert_args(f('jack 23 unexpected-arg'), expected_positional)


def test_convert_args_fails_with_too_few_positionals():
    expected_positional = ['name!', 'age!']
    with pytest.raises(CmdArgException):
        convert_args(f('jack'), expected_positional)


def test_convert_args_handles_correct_required_positionals():
    expected_positional = ['name!', 'age!']
    final_args = convert_args(f('jack 23'), expected_positional)
    assert final_args == {'name': 'jack', 'age': '23'}


def test_convert_args_handles_non_required_positionals():
    expected_positional = ['name', 'age']
    final_args = convert_args(f('jack 23'), expected_positional)
    assert final_args == {'name': 'jack', 'age': '23'}
    final_args = convert_args(f('jack'), expected_positional)
    assert final_args == {'name': 'jack'}
    final_args = convert_args(f(''), expected_positional)
    assert final_args == {}


def test_convert_args_handles_some_required_positionals():
    expected_positional = ['name!', 'age']
    final_args = convert_args(f('jack 23'), expected_positional)
    assert final_args == {'name': 'jack', 'age': '23'}
    final_args = convert_args(f('jack'), expected_positional)
    assert final_args == {'name': 'jack'}
    with pytest.raises(CmdArgException):
        convert_args(f(''), expected_positional)
