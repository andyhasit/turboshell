import pytest
from turboshell.arg_utils import convert_args, CmdArgException
from .utils import f


def test_fails_with_unknown_named_arg():
    expected = ['name']
    with pytest.raises(CmdArgException) as e:
        convert_args(f('-age 23'), expected_named=expected)
    assert str(e.value) == 'Unexpected named arguments: age'


def test_fails_with_missing_required_named_arg():
    expected = ['name!', 'age']
    with pytest.raises(CmdArgException) as e:
        convert_args(f('-age 23'), expected_named=expected)
    assert str(e.value) == 'Named arguments expected but not supplied: name'


def test_works_with_one_required_arg():
    expected = ['name!', 'age']
    final_args = convert_args(f('-name jo'), expected_named=expected)
    assert final_args == {'name': 'jo'}


def test_works_with_combination_of_required():
    expected = ['name!', 'int:age']
    final_args = convert_args(f('-name jo -age 23'), expected_named=expected)
    assert final_args == {'name': 'jo', 'age': 23}
