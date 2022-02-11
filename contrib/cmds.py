"""
This is the module where you define your commands.

"""
from turboshell import ts

if ts.is_collecting:
    print("Collecting definitions")
    ts.alias("test", "echo foo")


@ts.cmd(alias="test.bar")
def bar():
    print("baaa")



