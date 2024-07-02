# pip install .
from setuptools import setup

setup(
    name = "my_project",
    version = "Beta",
    author = "Ivan Giove",
    description = "Per adesso ancora nulla",
    python_requires = ">=3.6",
    install_requires = [
        "networkx",
        "matplotlib",
        "scipy"
    ]
)