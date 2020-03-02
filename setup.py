from setuptools import setup
from pathlib import Path
from typing import Dict

HERE = Path(__file__).parent

version: Dict[str, str] = {}
version_file = HERE / "src" / "thermostate" / "_version.py"
exec(version_file.read_text(), version)

setup(version=version["__version__"], package_dir={"": "src"})
