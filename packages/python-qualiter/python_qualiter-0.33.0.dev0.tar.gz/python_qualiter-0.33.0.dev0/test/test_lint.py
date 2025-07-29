"""
Unit test for the lint module.

This module contains test for the linting functionality, including:
- LinterConfig class
- run_linter function
- get_linter_configs function
- lint_file function

Each test verifies a specific aspect of the linting system to ensure
it correctly identifies and reports code quality issues.
"""

from unittest import mock

import pytest

from src.lint import (
    LinterConfig,
    expand_file_patterns,
    get_linter_configs,
    lint_file,
    run_linter,
)


@pytest.fixture(name="test_directory")
def get_test_directory(tmp_path):
    """Create a test directory structure with Python files for testing."""
    # Create a test directory structure
    py_file1 = tmp_path / "test1.py"
    py_file1.write_text("print('test1')")

    py_file2 = tmp_path / "test2.py"
    py_file2.write_text("print('test2')")

    subdir = tmp_path / "subdir"
    subdir.mkdir()

    py_file3 = subdir / "test3.py"
    py_file3.write_text("print('test3')")

    # Create a venv directory that should be excluded
    venv_dir = tmp_path / "venv"
    venv_dir.mkdir()

    venv_file = venv_dir / "venv_file.py"
    venv_file.write_text("print('venv')")

    # Return a dictionary of paths for easy access in test
    return {
        "tmp_path": tmp_path,
        "py_file1": py_file1,
        "py_file2": py_file2,
        "py_file3": py_file3,
        "subdir": subdir,
        "venv_dir": venv_dir,
        "venv_file": venv_file,
    }


@pytest.fixture(name="sample_py_file")
def get_sample_py_file(tmp_path):
    """Create a sample Python file for testing."""
    file_path = tmp_path / "test_sample.py"
    file_path.write_text("def test_function():\n    pass\n")
    return str(file_path)


def test_linter_config():
    """Test LinterConfig class."""
    config = LinterConfig(name="test", cmd_base=["test_cmd"], options=["--option"])
    assert config.name == "test"
    assert config.cmd_base == ["test_cmd"]
    assert config.options == ["--option"]

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


def test_run_linter_command_not_found():
    """Test run_linter with a command that doesn't exist."""
    with mock.patch("shutil.which", return_value=None):
        success, output = run_linter(["nonexistent_command"])

        assert success is False
        assert "not found in PATH" in output


def test_get_linter_configs():
    """Test get_linter_configs returns the expected linters."""
    configs = get_linter_configs()

    # Check that we have all expected linters
    linter_names = [config.name for config in configs]
    expected_linters = ["isort", "black", "mypy", "flake8", "pylint", "vulture", "ruff"]

    for linter in expected_linters:
        assert linter in linter_names


def test_lint_file(sample_py_file):
    """Test lint_file with a sample Python file."""
    with mock.patch("src.lint.run_linter") as mock_run_linter:
        # Mock successful linter run
        mock_run_linter.return_value = (True, "Success output")

        results = lint_file(sample_py_file)

        # Check that all linters ran successfully
        assert len(results) == 7  # Assuming 7 linters
        for result in results:
            assert result.success is True
            assert result.output == "Success output"


def test_expand_file_patterns_specific_file(test_directory):
    """Test expand_file_patterns with a specific file."""
    result = expand_file_patterns([str(test_directory["py_file1"])])
    assert len(result) == 1
    assert str(test_directory["py_file1"]) in result


def test_expand_file_patterns_wildcard(test_directory):
    """Test expand_file_patterns with wildcard patterns."""
    result = expand_file_patterns([str(test_directory["tmp_path"] / "*.py")])
    assert len(result) == 2
    assert str(test_directory["py_file1"]) in result
    assert str(test_directory["py_file2"]) in result


def test_expand_file_patterns_directory(test_directory):
    """Test expand_file_patterns with directory (should recursively find all .py files)."""
    result = expand_file_patterns([str(test_directory["tmp_path"])])
    assert len(result) == 3  # Should exclude venv file
    assert str(test_directory["py_file1"]) in result
    assert str(test_directory["py_file2"]) in result
    assert str(test_directory["py_file3"]) in result
    assert str(test_directory["venv_file"]) not in result


def test_expand_file_patterns_multiple_patterns(test_directory):
    """Test expand_file_patterns with multiple patterns."""
    result = expand_file_patterns(
        [str(test_directory["py_file1"]), str(test_directory["subdir"])]
    )
    assert len(result) == 2
    assert str(test_directory["py_file1"]) in result
    assert str(test_directory["py_file3"]) in result
