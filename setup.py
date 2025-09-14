from setuptools import setup, find_packages

# Package configuration for setuptools
setup(
    # Name of your package (shown on PyPI if published)
    name="todo-app",
    # Version of your package
    version="0.1.0",
    # Automatically discover all packages in the project directory
    packages=find_packages(),
    # Define entry points for command-line scripts
    entry_points={
        "console_scripts": [
            # This creates a command `todo` in the terminal
            # When run, it calls the `main()` function from todolist/main.py
            "todo = todolist.main:main",  # command = package.module:function
        ],
    },
    # Minimum Python version required
    python_requires=">=3.7",
)