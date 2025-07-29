import setuptools
from pathlib import Path

long_desc = Path("README.md").read_text()
setuptools.setup(
    name="CalculadoraMUYBASICA",
    version="1.0",
    long_description=long_desc,
    packages=setuptools.find_packages()
)
