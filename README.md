# ThermoState

This package provides a wrapper around [CoolProp](https://github.com/CoolProp/CoolProp) that integrates [Pint](https://pint.readthedocs.io) for easy thermodynamic state management in any unit system.

## Installation

### Conda

The preferred installation method is to use [`conda`](https://anaconda.com/download). Using Conda, ThermoState can be installed for either Python 3.6, or 3.7\. If you have an existing Conda environment with one of those Python versions, installing ThermoState can be done by

```bash
conda install -c bryanwweber thermostate conda-forge::pint
```

This installs Pint from the `conda-forge` channel; if you would like to use another channel to install Pint, change the `conda-forge` to be the name of the channel you prefer. If Pint is already installed in your environment, the `conda-forge::pint` can be omitted entirely.

If you do not have an environment with Python 3.6 or 3.7, you can create a new environment with

```bash
conda create -n thermostate -c bryanwweber thermostate conda-forge::pint
```

### Pip

Alternatively, ThermoState can be installed with pip.

```bash
pip install thermostate
```

### From Source

ThermoState is a pure-Python package that supports any Python version 3.6 and higher. To install from source, clone the source code repository and install using `pip`.

```bash
git clone https://github.com/bryanwweber/thermostate
cd thermostate
pip install .
```

## Documentation

Documentation can be found at <https://bryanwweber.github.io/thermostate/>. The documentation contains a short [tutorial](https://bryanwweber.github.io/thermostate/Tutorial.html), [examples](https://bryanwweber.github.io/thermostate/examples.html), and [API documentation](https://bryanwweber.github.io/thermostate/thermostate.html) for the package.

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

[![codecov](https://codecov.io/gh/bryanwweber/thermostate/branch/master/graph/badge.svg)](https://codecov.io/gh/bryanwweber/thermostate)[![Python package](https://github.com/bryanwweber/thermostate/workflows/Python%20package/badge.svg)](https://github.com/bryanwweber/thermostate/actions?query=workflow%3A%22Python+package%22)

## Anaconda Package Version

[![Anaconda-Server Badge Version](https://anaconda.org/bryanwweber/thermostate/badges/version.svg)](https://anaconda.org/bryanwweber/thermostate) [![Anaconda-Server Badge Downloads](https://anaconda.org/bryanwweber/thermostate/badges/downloads.svg)](https://anaconda.org/bryanwweber/thermostate)
