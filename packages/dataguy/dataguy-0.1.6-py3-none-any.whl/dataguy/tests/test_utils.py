import os
import pytest
from dataguy.utils import validate_file_path, LLMResponseCache


def test_validate_file_path(mocker, tmp_path):
    # Create a temporary file
    temp_file = tmp_path / "test_file.txt"
    temp_file.write_text("Sample content")

    mocker.patch("builtins.open", side_effect=PermissionError)

    with pytest.raises(PermissionError):
        validate_file_path(str(temp_file))

    # Test valid file path
    assert validate_file_path(str(temp_file)) is True

    # Test file not found
    with pytest.raises(FileNotFoundError):
        validate_file_path(str(tmp_path / "non_existent_file.txt"))

    # Test file not readable
    temp_file.chmod(0o000)  # Remove read permissions
    with pytest.raises(PermissionError):
        validate_file_path(str(temp_file))
    temp_file.chmod(0o644)  # Restore permissions


def test_llm_response_cache():
    cache = LLMResponseCache()

    # Test set and get
    cache.set("prompt1", "response1")
    assert cache.get("prompt1") == "response1"
    assert cache.get("non_existent_prompt") is None

    # Test get_or_set with existing prompt
    assert cache.get_or_set("prompt1", lambda x: "new_response") == "response1"

    # Test get_or_set with new prompt
    assert cache.get_or_set("prompt2", lambda x: "response2") == "response2"
    assert cache.get("prompt2") == "response2"

    # Test save_to_file and load_from_file
    temp_file = "test_cache.json"
    cache.save_to_file(temp_file)
    assert os.path.exists(temp_file)

    new_cache = LLMResponseCache()
    new_cache.load_from_file(temp_file)
    assert new_cache.get("prompt1") == "response1"
    assert new_cache.get("prompt2") == "response2"

    # Clean up
    os.remove(temp_file)