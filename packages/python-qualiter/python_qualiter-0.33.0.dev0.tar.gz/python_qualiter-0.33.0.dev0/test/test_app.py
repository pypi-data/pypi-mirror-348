"""
This test file is a part of the linting utility for Python code.
"""

from unittest import mock

import pytest

from src.lint import LinterConfig, get_linter_configs, run_linter


@pytest.fixture
def sample_py_file(tmp_path):
    """Create a sample Python file for testing."""
    file_path = tmp_path / "test_sample.py"
    file_path.write_text("def test_function():\n    pass\n")
    return str(file_path)


def test_linter_config_creation():
    """Test creating a LinterConfig object."""
    config = LinterConfig(name="test", cmd_base=["test_cmd"], options=["--option"])
    assert config.name == "test"
    assert config.cmd_base == ["test_cmd"]
    assert config.options == ["--option"]


def test_linter_config_get_command():
    """Test the get_command method of LinterConfig."""
    config = LinterConfig(name="test", cmd_base=["test_cmd"], options=["--option"])
    cmd = config.get_command("file.py")
    assert cmd == ["test_cmd", "file.py", "--option"]


def test_run_linter_success():
    """Test run_linter with a successful command."""
    with mock.patch("subprocess.run") as mock_run:
        mock_run.return_value = mock.Mock(
            returncode=0, stdout="Success output", stderr=""
        )

        success, output = run_linter(["echo", "test"])

        assert success is True
        assert output == "Success output"
        mock_run.assert_called_once()


def test_run_linter_failure():
    """Test run_linter with a failing command."""
    with mock.patch("subprocess.run") as mock_run:
        mock_run.return_value = mock.Mock(
            returncode=1, stdout="", stderr="Error output"
        )

        success, output = run_linter(["echo", "test"])

        assert success is False
        assert output == "Error output"
        mock_run.assert_called_once()


def test_get_linter_configs():
    """Test that get_linter_configs returns the expected linters."""
    configs = get_linter_configs()
    linter_names = [config.name for config in configs]
    expected_linters = ["isort", "black", "mypy", "flake8", "pylint", "vulture"]
    for linter in expected_linters:
        assert linter in linter_names
