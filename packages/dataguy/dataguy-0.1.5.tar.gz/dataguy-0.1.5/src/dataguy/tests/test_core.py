import pytest
import pandas as pd
from dataguy.core import DataGuy

def test_initialize():
    """Test initialization of DataGuy with default and custom parameters."""
    dg = DataGuy()
    assert dg.data is None
    assert dg.context.max_code_history == 100

    dg_custom = DataGuy(max_code_history=50)
    assert dg_custom.context.max_code_history == 50

def test_set_data():
    """Test setting data in DataGuy."""
    dg = DataGuy()
    df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    dg.set_data(df)
    assert dg.data.equals(df)

    # Test with a dictionary
    data_dict = {"a": [1, 2, 3], "b": [4, 5, 6]}
    dg.set_data(data_dict)
    assert dg.data.equals(pd.DataFrame(data_dict))

    # Test with unsupported data type
    with pytest.raises(TypeError):
        dg.set_data("invalid data type")

def test_summarize_data():
    """Test summarizing data."""
    dg = DataGuy()
    df = pd.DataFrame({"a": [1, 2, 3], "b": [4, None, 6]})
    dg.set_data(df)
    summary = dg.summarize_data()

    assert summary["shape"] == (3, 2)
    assert summary["columns"] == ["a", "b"]
    assert summary["missing_counts"] == {"a": 0, "b": 1}
    assert summary["means"] == {"a": 2.0, "b": 5.0}

def test_describe_data(mocker):
    """Test describing data using LLM."""
    dg = DataGuy()
    df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    dg.set_data(df)

    # Mock the LLM response
    mocker.patch("dataguy.core.Chat", return_value=mocker.Mock(__call__=mocker.Mock(return_value=mocker.Mock(content=[mocker.Mock(text="This is a test description.")]))))
    description = dg.describe_data()

    assert description == "This is a test description."