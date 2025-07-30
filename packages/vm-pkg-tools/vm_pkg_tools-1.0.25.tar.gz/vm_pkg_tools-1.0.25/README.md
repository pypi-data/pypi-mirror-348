# README: vm-pkg-tools

## Overview

`vm-pkg-tools` is a Python package designed to facilitate parsing scout files for volleyball analytics. This package provides robust parsing capabilities for DVW scout files, including proper handling of special characters, point-by-point action tracking, and comprehensive match data extraction.

## Features

- Robust DVW scout file parsing
- Proper handling of special characters (German umlauts, etc.)
- Point-by-point action tracking with sequential IDs
- Comprehensive match data extraction
- Support for multiple sets and lineups
- Detailed action parsing with skill types and results

## Directory Structure

```bash
project_root/
├── data/
│   └── scouts/
│       └── &1003.dvw
├── src/
│   ├── vm_pkg_tools/
│   │   ├── core/
│   │   │   ├── main.py          # Main entry point
│   │   │   └── orchestrator.py  # Core parsing logic
│   │   ├── parsers/
│   │   │   ├── match_actions/   # Point and action parsing
│   │   │   ├── lineups/         # Team lineup parsing
│   │   │   └── players/         # Player information parsing
│   │   ├── utils/
│   │   │   ├── file_utils.py    # File handling utilities
│   │   │   ├── parser_utils.py  # Common parsing utilities
│   │   │   └── logger.py        # Logging configuration
│   │   └── validators/          # Data validation
├── tests/
├── README.md
├── requirements.txt
├── setup.py
└── dist/
```

## Requirements

### Runtime Dependencies

- `click>=8.1,<9.0`
- `pydantic>=2.0,<3.0`
- `sqlalchemy>=2.0,<3.0`
- `PyYAML>=6.0,<7.0`
- `unidecode>=1.3,<2.0`
- `chardet>=5.0,<6.0`
- `colorlog>=6.0,<7.0`
- `jsonschema>=4.0,<5.0`

### Development and Testing Dependencies

- `black>=24.10`
- `flake8>=7.1`
- `isort>=5.13`
- `pylint>=3.3`
- `pytest>=8.3.4`
- `attrs>=24.3`
- `twine`
- `setuptools`

## Installation

### Install Locally for Testing

1. Build the package:

   ```bash
   python setup.py sdist bdist_wheel
   ```

2. Install the package in a virtual environment:

   ```bash
   python -m venv test_env
   source test_env/bin/activate
   pip install dist/vm_pkg_tools-<version>-py3-none-any.whl
   ```

3. Verify installation:
   ```bash
   vmtools-cli --help
   ```

## Usage

### Basic Usage

Parse a scout file:

```bash
vmtools-cli parse data/scouts/&1003.dvw
```

## Recent Updates

### Version 1.0.24

- Fixed encoding issues with special characters (German umlauts)
- Improved point ID generation for sequential tracking
- Enhanced action parsing with proper service detection
- Added support for proper action sequencing within points

## Testing

1. Create a fresh virtual environment:

   ```bash
   python -m venv test_env
   source test_env/bin/activate
   ```

2. Install the built package:

   ```bash
   pip install dist/vm_pkg_tools-<version>-py3-none-any.whl
   ```

3. Run tests:
   ```bash
   pytest tests/
   ```

## Deployment

1. Remove old build artifacts:

   ```bash
   rm -rf build/ dist/ *.egg-info
   ```

2. Build the package:

   ```bash
   python setup.py sdist bdist_wheel
   ```

3. Upload to PyPI:
   ```bash
   twine upload dist/*
   ```

## Versioning

### Tagging a Release

```bash
git tag v<version>
git push origin v<version>
```

## Common Issues

### Encoding Issues

- If you encounter encoding issues with special characters, ensure the input file is properly encoded
- The parser now handles German umlauts and other special characters correctly

### Missing Actions

- If actions are missing from points, check that the scout file follows the correct format
- Actions should be listed before the point line
- Service actions should be marked with 'S' in the skill type

### Import Errors

- Verify all imports use the correct relative paths
- Update `PYTHONPATH` if necessary

## License

This project is licensed under a **Custom Proprietary License**.

The use of this software is strictly prohibited for any of the following purposes without prior written consent from the author:

- Commercial use
- Redistribution or sublicensing
- Modification or derivation for other applications or platforms

By accessing this software, you agree to adhere to the terms outlined in the [LICENSE](LICENSE) file. For further details, see the [COPYRIGHT](COPYRIGHT) file.

For licensing inquiries, please contact the author:  
**Reza Barzegar Gashti**  
[rezabarzegargashti@gmail.com](mailto:rezabarzegargashti@gmail.com)
