# ThermoState

This package provides a wrapper around [CoolProp](https://github.com/CoolProp/CoolProp) that integrates [Pint](https://pint.readthedocs.io) for easy thermodynamic state management in any unit system.

## Installation

### Conda

The preferred installation method is to use [conda](https://anaconda.com/download). Using Conda, ThermoState can be installed for Python 3.9 and up. You can create a new environment with:

```shell
conda create -n thermostate -c conda-forge thermostate
```

### Pip

Alternatively, ThermoState can be installed with `pip`.

```shell
python -m pip install thermostate
```

### From Source

ThermoState is a pure-Python package that supports any Python version 3.9 and higher. To install from source, clone the source code repository and install using `pip`.

```shell
git clone https://github.com/bryanwweber/thermostate
cd thermostate
python -m pip install .
```

## Documentation

Documentation can be found at <https://thermostate.readthedocs.io/>. The documentation contains a short [tutorial](https://thermostate.readthedocs.io/en/stable/Tutorial.html), [examples](https://thermostate.readthedocs.io/en/stable/examples.html), and [API documentation](https://thermostate.readthedocs.io/en/stable/thermostate.html) for the package.

[![Documentation Status](https://readthedocs.org/projects/thermostate/badge/?version=stable)](https://thermostate.readthedocs.io/en/stable/?badge=stable)

## Citation

If you have used ThermoState in your work, we would appreciate including a citation to the software! ThermoState has been published in [JOSE](https://jose.theoj.org/), available at the link below.

[![DOI](https://jose.theoj.org/papers/10.21105/jose.00033/status.svg)](https://doi.org/10.21105/jose.00033)

For those using Bib(La)TeX, you can use the following entry

```bibtex
@article{weber_thermostate_2018,
    title = {{ThermoState}: {A} state manager for thermodynamics courses},
    volume = {1},
    issn = {2577-3569},
    shorttitle = {{ThermoState}},
    url = {https://jose.theoj.org/papers/10.21105/jose.00033},
    doi = {10.21105/jose.00033},
    number = {8},
    urldate = {2018-10-24},
    journal = {Journal of Open Source Education},
    author = {Weber, Bryan},
    month = oct,
    year = {2018},
    pages = {33}
}
```

## Code of Conduct & Contributing

We welcome contributions from anyone in the community. Please look at the [Contributing instructions](https://github.com/bryanwweber/thermostate/blob/master/CONTRIBUTING.md) for more information. This project follows the [Contributor Covenant Code of Conduct](https://github.com/bryanwweber/thermostate/blob/master/CODE_OF_CONDUCT.md), version 1.4\. In short, be excellent to each other.

## Continuous Integration Status

[![codecov](https://codecov.io/gh/bryanwweber/thermostate/branch/master/graph/badge.svg)](https://codecov.io/gh/bryanwweber/thermostate)[![Python package](https://github.com/bryanwweber/thermostate/actions/workflows/pythonpackage.yml/badge.svg)](https://github.com/bryanwweber/thermostate/actions/workflows/pythonpackage.yml)

## Anaconda Package Version

[![Anaconda-Server Badge Version](https://anaconda.org/conda-forge/thermostate/badges/version.svg)](https://anaconda.org/conda-forge/thermostate) [![Anaconda-Server Badge Downloads](https://anaconda.org/conda-forge/thermostate/badges/downloads.svg)](https://anaconda.org/conda-forge/thermostate)
