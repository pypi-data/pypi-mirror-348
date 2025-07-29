# Python Code Linting Tool

A modern Click-based CLI tool for running multiple linting tools on Python files with a clean visual output.

## Features

- **Multiple Linters**: Runs isort, black, mypy, flake8, pylint, and vulture in a single command
- **Visual Matrix**: Displays results in a clean matrix format with files as rows and linters as columns
- **Auto-fix Mode**: Automatically applies fixes for isort and black
- **Linter Selection**: Enable or disable specific linters as needed
- **Detailed Reporting**: Option to show detailed failure information
- **Installation Checking**: Verify if all required linters are installed
- **Recursive Search**: Automatically finds all Python files in directories and subdirectories (excluding virtual environments)

## Installation

1. Clone this repository:
   ```
   git clone https://gitlab.com/rbacovic/python_qualiter.git
   cd python_qualiter
   ```

2. Ensure you have Python 3.7+ installed.

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
   
4. Make the script executable:
   ```
   cd src
   chmod +x app.py
   ```

## Usage

### Basic Linting

Run linting on Python files:

```bash
./app.py lint path/to/your/file.py
```

Run on multiple files or using wildcards:

```bash
./app.py lint file1.py file2.py
./app.py lint folder/*.py
```

Run on a directory (recursively checks all Python files):

```bash
./app.py lint your_project_folder/
```

### Command Options

**Linting Command:**

```bash
./app.py lint [OPTIONS] FILES...
```

Options:
- `-v, --verbose`: Show detailed output during linting
- `-d, --details`: Show detailed failure messages after the results matrix
- `-e, --enable TEXT`: Enable only specific linters (can be used multiple times)
- `-x, --disable TEXT`: Disable specific linters (can be used multiple times)
- `-f, --fix`: Apply auto-fixes where possible (currently for isort and black)
- `-c, --config PATH`: Path to configuration file (for future implementation)
- `--help`: Show help message

**Info Command:**

```bash
./app.py info [OPTIONS]
```

Options:
- `--list-linters`: List all available linters
- `--check-installs`: Check if all linters are installed
- `--help`: Show help message

### Examples

Check all linters and show detailed errors:
```bash
./app.py lint my_file.py --details
```

Only run specific linters:
```bash
./app.py lint my_file.py --enable black --enable isort
```

Disable specific linters:
```bash
./app.py lint my_file.py --disable pylint
```

Auto-fix issues (where possible):
```bash
./app.py lint my_file.py --fix
```

Check if all linters are installed:
```bash
./app.py info --check-installs
```

Lint an entire project directory (recursively):
```bash
./app.py lint my_project/ --fix
```

## Output Format

The tool displays a matrix with files as rows and linters as columns:

```
===========================================================================
LINTING RESULTS MATRIX
===========================================================================
File                                     | black    | flake8   | isort    | mypy     | pylint   | vulture  
---------------------------------------------------------------------------
my_file.py                               | ✅       | ✅       | ✅       | ❌       | ✅       | ✅       
another_file.py                          | ✅       | ❌       | ✅       | ✅       | ❌       | ✅       
===========================================================================
❌ 3 FAILURES OUT OF 12 CHECKS
===========================================================================
```

If you use the `--details` option, you'll also see detailed failure information:

```
===========================================================================
DETAILED FAILURE INFORMATION
===========================================================================

File: my_file.py
---------------------------------------------------------------------------

mypy found issues:
my_file.py:42: error: Incompatible types in assignment (expression has type "str", variable has type "int")

File: another_file.py
---------------------------------------------------------------------------

flake8 found issues:
another_file.py:15:80: E501 line too long (88 > 79 characters)

pylint found issues:
another_file.py:27:0: C0103: Variable name "x" doesn't conform to snake_case naming style (invalid-name)
```

## Supported Linters

| Linter   | Purpose                 | Auto-fix Support |
|----------|-------------------------|-----------------|
| [isort](https://pycqa.github.io/isort/)    | Sort imports            | Yes             |
| [black](https://black.readthedocs.io/en/stable/)    | Format code             | Yes             |
| [mypy](https://mypy.readthedocs.io/en/stable/)     | Type checking           | No              |
| [flake8](https://flake8.pycqa.org/en/latest/)   | Style guide enforcement | No              |
| [pylint](https://pylint.pycqa.org/en/latest/)   | Static code analysis    | No              |
| [vulture](https://github.com/jendrikseipp/vulture)  | Dead code detection     | No              |

## Configuration

Currently, the tool uses default configurations for each linter. A future update will add support for custom configuration files using the `--config` option.

## Extending

To add a new linter:

1. Open `lint.py`
2. Add your linter configuration to the `get_linter_configs()` function:
   ```python
   LinterConfig(
       name="new_linter",
       cmd_base=["new_linter_command"],
       options=["--your-option", "value"]
   )
   ```

## Troubleshooting

If you encounter issues:

1. Make sure all linters are installed:
   ```
   ./app.py info --check-installs
   ```

2. Run in verbose mode for more detailed output:
   ```
   ./app.py lint my_file.py --verbose
   ```

3. If your file paths contain spaces, make sure to quote them:
   ```
   ./app.py lint "path with spaces/my_file.py"
   ```

4. If no files are found, check that your patterns are correct:
   ```
   ./app.py lint my_folder/*.py --verbose
   ```

5. If you see errors about missing linters, install them individually:
   ```
   pip install isort black mypy flake8 pylint vulture
   ```

## Testing

Run the tests to ensure everything is working correctly:

```bash
pytest -v test_app.py test_lint.py
```

For more detailed test output:

```bash
pytest -s -vv -x
```

## License

[MIT License](LICENSE)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests to ensure they pass
5. Commit your changes (`git commit -m 'Add some amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request
