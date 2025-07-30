from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="tempmail-cli",
    version="2025.5.7",
    description="A command-line tool for managing temporary email accounts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="hasanfq6",
    author_email="hasanfq818@gmail.com",
    packages=find_packages(),
    py_modules=["tempmail_cli"],
    install_requires=[
        "requests",
        "tabulate",
    ],
    entry_points={
        "console_scripts": [
            "tempmail=tempmail_cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
) 
