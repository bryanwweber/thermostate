from setuptools import setup
from pathlib import Path
from typing import Dict

HERE = Path(__file__).parent

version: Dict[str, str] = {}
version_file = HERE / "src" / "thermostate" / "_version.py"
exec(version_file.read_text(), version)

readme = (HERE / "README.md").read_text()
changelog = (HERE / "CHANGELOG.md").read_text()

long_description = readme + "\n\n" + changelog

install_requires = ["coolprop>=6.1.0,<6.3", "pint>=0.7.2,<0.10"]

tests_require = ["pytest>=3.0.0", "pytest-cov>=2.3.1"]

setup(
    name="thermostate",
    version=version["__version__"],
    description="A package to manage thermodynamic states",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bryanwweber/thermostate",
    author="Bryan W. Weber",
    author_email="bryan.w.weber@gmail.com",
    license="BSD-3-clause",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Operating System :: MacOS",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Operating System :: Microsoft :: Windows :: Windows 7",
        "Operating System :: Microsoft :: Windows :: Windows 8",
        "Operating System :: Microsoft :: Windows :: Windows 8.1",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: Linux",
    ],
    packages=["thermostate"],
    package_dir={"": "src"},
    install_requires=install_requires,
    tests_require=tests_require,
    python_requires="~=3.6",
)
