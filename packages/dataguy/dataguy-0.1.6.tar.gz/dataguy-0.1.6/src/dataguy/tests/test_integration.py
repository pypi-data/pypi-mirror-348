import pytest
import pandas as pd
from dataguy.core import DataGuy

@pytest.fixture
def sample_data():
    """Fixture to provide sample data for testing."""
    return pd.DataFrame({
        "age": [25, 30, None, 45, 50, None],
        "score": [88, 92, 75, None, 85, 90]
    })

@pytest.fixture
def data_guy():
    """Fixture to provide a DataGuy instance."""
    return DataGuy(max_code_history=50)

def test_set_data(data_guy, sample_data):
    """Test setting data in DataGuy."""
    data = data_guy.set_data(sample_data)
    assert data.equals(sample_data), "Data was not set correctly."

def test_summarize_data(data_guy, sample_data):
    """Test summarizing data."""
    data_guy.set_data(sample_data)
    summary = data_guy.summarize_data()
    assert summary["shape"] == (6, 2), "Shape summary is incorrect."
    assert "age" in summary["columns"], "Columns summary is missing 'age'."
    assert summary["missing_counts"]["age"] == 2, "Missing counts for 'age' are incorrect."

def test_wrangle_data(data_guy, sample_data):
    """Test wrangling data."""
    data_guy.set_data(sample_data)
    cleaned_data = data_guy.wrangle_data()
    assert cleaned_data.isna().sum().sum() == 0, "Wrangling did not handle missing values correctly."

def test_plot_data(data_guy, sample_data):
    """Test plotting data."""
    data_guy.set_data(sample_data)
    try:
        data_guy.plot_data("age", "score")
    except Exception as e:
        pytest.fail(f"Plotting failed with error: {e}")

def test_model_selection_behavior(capfd):
    small_data = pd.DataFrame({"a": range(10), "b": range(10)})
    large_data = pd.DataFrame({"a": range(120000), "b": range(120000)})

    dg_small = DataGuy()
    dg_small.set_data(small_data)
    dg_small.wrangle_data()
    out_small, _ = capfd.readouterr()
    assert "Switching to 'haiku'" not in out_small

    dg_large = DataGuy()
    dg_large.set_data(large_data)
    dg_large.wrangle_data()
    out_large, _ = capfd.readouterr()
    assert "Switching to 'haiku'" in out_large

    dg_override = DataGuy(model_overrides={"code": "claude-3-haiku-20240307"})
    dg_override.set_data(small_data)
    dg_override.wrangle_data()