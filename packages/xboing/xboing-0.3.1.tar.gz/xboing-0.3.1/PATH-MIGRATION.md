# Python Package Path Migration Guide for PyPI Distribution

## Understanding the Issue

When distributing Python packages via PyPI, it's crucial to structure your package correctly to ensure it works both during development and after installation. Based on analysis of the xboing-python project, the following issues have been identified:

1. **In development mode with hatch**: Everything works fine
2. **After pip installation**: 
   - You need to run `python -m src.Xboing` instead of just `python -m Xboing`
   - Imports fail because Python looks for modules like `src.ui` instead of just `ui`

This indicates a package structure issue where the package namespace doesn't align with how Python expects packages to be organized after installation.

## Current Project Structure

The current xboing-python project structure is:

```
xboing-python/
├── pyproject.toml
├── README.md
├── src/
│   ├── __init__.py          # Imports from .xboing import main
│   ├── __version__.py
│   ├── app_coordinator.py
│   ├── controllers/
│   ├── di_module.py
│   ├── engine/
│   ├── game/
│   ├── layout/
│   ├── renderers/
│   ├── ui/
│   ├── utils/
│   └── xboing.py            # Main entry point with the main() function
└── tests/
```

The current pyproject.toml configuration includes:

```toml
[project]
name = "Xboing"
# ...

[project.scripts]
xboing = "xboing:main"

[tool.hatch.build.targets.wheel]
packages = ["src"]
```

## Core Issues

1. **Package Structure**: Modules are placed directly under `src/` instead of within a proper package directory.
2. **Import Style**: Imports use absolute paths (e.g., `from app_coordinator import AppCoordinator`).
3. **Configuration**: `packages = ["src"]` makes pip install from `src/` to `site-packages/src/`.
4. **Namespace Inconsistency**: `name = "Xboing"` in pyproject.toml doesn't match import patterns.

## Python Package Best Practices

### Recommended Package Structure

The recommended structure for Python packages follows the "src layout":

```
xboing-python/             # Project directory
├── pyproject.toml         # Project metadata and build configuration
├── README.md              # Project documentation
├── src/                   # Source directory (not importable)
│   └── xboing/            # Package directory (same name as distribution)
│       ├── __init__.py    # Makes the directory a package and exports main
│       ├── __main__.py    # Entry point for running with python -m xboing
│       ├── app_coordinator.py
│       ├── controllers/
│       └── ...            # Other modules and sub-packages
└── tests/                 # Test directory
```

### Key Python Packaging Principles

1. **Namespace Consistency**: Your distribution name, import path, and directory structure should match.
2. **src Layout**: The src directory itself is not importable, but contains your package(s).
3. **Relative Imports**: Modules within a package should use relative imports.
4. **Proper Entry Points**: Use project.scripts to create command-line entry points.

## Detailed Migration Plan for xboing-python

### Step 1: Create the New Package Structure

1. Create a new directory `src/xboing/`.
2. Move all Python modules and packages from `src/` to `src/xboing/`.
3. Create/update `src/xboing/__init__.py` to export the main function:

```python
"""XBoing package root."""

from .xboing import main
```

4. Create `src/xboing/__main__.py` to enable running as a module:

```python
"""Entry point for running as python -m xboing."""

from .xboing import main

if __name__ == "__main__":
    main()
```

### Step 2: Update pyproject.toml

1. Change the package name to lowercase for consistency:

```toml
[project]
name = "xboing"
```

2. Update the packages setting:

```toml
[tool.hatch.build.targets.wheel]
packages = ["src/xboing"]
```

3. Update the entry point:

```toml
[project.scripts]
xboing = "xboing.xboing:main"
```

4. Update the version path:

```toml
[tool.hatch.version]
path = "src/xboing/__version__.py"
```

5. Update any other paths in the configuration that reference the src directory.

### Step 3: Fix Import Statements

1. Convert all absolute imports to relative imports or fully qualified imports.

For example, in `xboing.py`, change:
```python
from app_coordinator import AppCoordinator
from controllers.controller import Controller
```

To either relative imports:
```python
from .app_coordinator import AppCoordinator
from .controllers.controller import Controller
```

Or fully qualified imports:
```python
from xboing.app_coordinator import AppCoordinator
from xboing.controllers.controller import Controller
```

2. Check all modules in your package and update imports accordingly.

3. Pay special attention to:
   - Circular imports (they may need restructuring)
   - Type checking imports (they may need special handling)
   - Module-level imports vs function-level imports

### Step 4: Update Resources and Asset Paths

1. Ensure all resource and asset paths use package-relative paths:

```python
from importlib import resources

def get_asset_path(asset_name):
    with resources.path('xboing.resources', asset_name) as path:
        return path
```

2. Update any code that assumes a specific directory structure.

### Step 5: Testing

1. Install the package in development mode:

```bash
cd xboing-python
pip install -e .
```

2. Test that running the package works:

```bash
python -m xboing
```

3. Test the entry point script:

```bash
xboing
```

4. Build a distribution and test installation:

```bash
python -m build
pip install dist/xboing-*.whl
python -c "import xboing; print(xboing.__file__)"
```

## Handling Special Cases

### Type Checking Imports

For type checking imports, continue using the TYPE_CHECKING approach, but update the imports:

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .controllers.controller_manager import ControllerManager
    from .ui.ui_manager import UIManager
```

### Relative vs. Absolute Imports

Generally prefer:
- Relative imports (`.module`) for importing from the same package
- Absolute imports (`xboing.module`) for imports from other parts of your package or for clarity

### Development vs. Production Environment Differences

When using the src layout:
- In development with hatch: The src directory is added to PYTHONPATH
- After installation: The package is installed to site-packages/xboing/

This difference is handled automatically by using the proper package structure and import patterns.

## Common Pitfalls to Avoid

1. **Mixed Import Styles**: Be consistent with import styles (all relative or all absolute).
2. **Hardcoded Paths**: Avoid absolute file paths in your code.
3. **Missing `__init__.py` Files**: Ensure every package directory has an `__init__.py` file.
4. **Using `sys.path` Manipulation**: Avoid modifying `sys.path` to find modules.
5. **Inconsistent Package Names**: Keep the same name across distribution, imports, and directories.

## Advantages of Proper Package Structure

1. **Reliable Imports**: Imports work the same way in development and production.
2. **Clean Namespace**: No risk of namespace collisions.
3. **Proper Entry Points**: Users can run the package as a command.
4. **Maintainability**: Easier to understand and maintain the codebase.
5. **Upgradability**: Easier to update dependencies and Python versions.

## Summary

By restructuring the xboing-python project to follow Python packaging best practices, you'll create a consistent, maintainable package that works reliably both in development and when installed via pip/PyPI. This migration involves moving files to create a proper package structure, updating imports to be consistent with that structure, and modifying the build configuration to correctly package and distribute the code.

After completing this migration, users will be able to install your package with pip and run it using either `python -m xboing` or simply `xboing`, and all imports within the package will work correctly without namespace issues.