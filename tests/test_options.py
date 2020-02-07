import pytest
from turboshell.arg_utils import convert_args, CmdArgException
from .utils import f


def test_fails_with_unknown_option():
    options = ['a', 's']
    with pytest.raises(CmdArgException) as e:
        convert_args(f('-ag'), expected_options=options)
    assert str(e.value) == 'Unexpected options: g'


def test_extracts_known_options():
    options = ['a', 's']
    final_args = convert_args(f('-s'), expected_options=options)
    assert final_args == {'options': ['s']}
