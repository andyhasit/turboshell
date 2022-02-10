
from turboshell import ts


if ts.is_collecting:
    ts.alias("test.foo", "echo foo")
    print('Collecting')


@ts.cmd(alias="test.bar")
def bar():
    print("baaa")



