from setuptools import setup, find_packages

setup(
    name="todo-app",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "todo = todolist.main:main",  # command = package.module:function
        ],
    },
    python_requires=">=3.7",
)