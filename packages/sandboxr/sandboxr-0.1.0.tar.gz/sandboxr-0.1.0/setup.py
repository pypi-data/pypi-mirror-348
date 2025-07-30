from setuptools import setup, find_packages

setup(
    name="sandboxr",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    entry_points={"console_scripts": ["pysand=pysand.cli:main"]},
)
