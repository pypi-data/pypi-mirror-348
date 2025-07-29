from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="tracecolor",
    version="0.5.0",
    author="Marco Del Pin",
    author_email="marco.delpin@gmail.com",
    description="A lightweight, colorized Python logger with TRACE and PROGRESS level support.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/marcodelpin/tracecolor",
    packages=find_packages(exclude=["tests.*", "tests"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "colorlog>=6.0.0",
    ],
)