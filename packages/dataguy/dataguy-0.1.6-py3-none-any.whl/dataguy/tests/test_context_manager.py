import pytest
import pandas as pd
import numpy as np
from dataguy.context_manager import ContextManager

def test_update_from_globals():
    context = ContextManager()
    globals_dict = {
        "df": pd.DataFrame({"a": [1, 2, 3]}),
        "arr": np.array([1, 2, 3]),
        "x": 42,
        "_private_var": "hidden",
        "func": lambda x: x,
    }
    context.update_from_globals(globals_dict)

    assert "df" in context.variables
    assert "arr" in context.variables
    assert "x" in context.variables
    assert "_private_var" not in context.variables
    assert "func" not in context.variables

def test_add_code():
    context = ContextManager(max_code_history=3)
    context.add_code("print('Hello')")
    context.add_code("x = 42")
    context.add_code("y = x + 1")
    context.add_code("z = y * 2")

    assert len(context.code_history) == 3
    assert context.code_history == ["x = 42", "y = x + 1", "z = y * 2"]

def test_get_context_summary():
    context = ContextManager()
    context.imported_packages = {"pandas", "numpy"}
    context.variables = {"df": "DataFrame(3, 2)", "x": "int"}
    context.code_history = ["x = 42", "df = pd.DataFrame({'a': [1, 2, 3]})"]

    summary = context.get_context_summary()
    assert "pandas" in summary
    assert "numpy" in summary
    assert "df: DataFrame(3, 2)" in summary
    assert "x: int" in summary
    assert "x = 42" in summary
    assert "df = pd.DataFrame({'a': [1, 2, 3]})" in summary