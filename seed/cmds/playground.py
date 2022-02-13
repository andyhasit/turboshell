"""
Use this module as a playground to experiment with turboshell.
"""
from turboshell import ts

ts.alias("test.1", "echo Testing 1", info="A simple alias")

@ts.cmd(alias="test.2", info="Calls a Python function")
def speak():
    print("Testing 2")
