# ThermoState

This package provides a wrapper around [CoolProp](https://github.com/CoolProp/CoolProp) that integrates [Pint](https://pint.readthedocs.io) for easy state management in any unit system.

## Installation

### Conda

The preferred installation method is to use [`conda`](https://anaconda.com/download). Using Conda, ThermoState can be installed for either Python 3.5 or 3.6. If you have an existing Conda environment with one of those Python versions, installing ThermoState can be done by

```bash
conda install -c bryanwweber thermostate conda-forge::pint
```

This installs Pint from the `conda-forge` channel; if you would like to use another channel to install Pint, or Pint is already installed in your environment, the `conda-forge::pint` can be omitted.

If you do not have an environment with Python 3.5 or 3.6, you can create a new environment with

```bash
conda create -n thermostate -c bryanwweber thermostate conda-forge::pint
```

### Pip

Alternatively, ThermoState can be installed with pip, for Python 3.5 only. This is because version 6.1.0 of CoolProp is only available for Python 3.5 from pip.

```bash
pip install thermostate
```

### From Source

ThermoState is a pure-Python package that supports any Python version 3.5 and higher. Binary installers for CoolProp (which has a C-extension for its Python interface) are only available for Python 3.5 (pip) and Pythons 3.5 and 3.6 (Conda). Other versions of Python can be supported by compiling CoolProp locally, for which instructions are available on the [CoolProp documentation](http://www.coolprop.org/dev/coolprop/wrappers/Python/index.html#manual-installation). Once CoolProp is installed, installing ThermoState can be done by

```bash
git clone https://github.com/bryanwweber/thermostate
cd thermostate
pip install .
```

## Documentation

<!-- markdownlint-disable MD034 -->
Documentation can be found at https://bryanwweber.github.io/thermostate/. The documentation contains a short [tutorial](https://bryanwweber.github.io/thermostate/Tutorial.html), [examples](https://bryanwweber.github.io/thermostate/examples.html), and [API documentation](https://bryanwweber.github.io/thermostate/thermostate.html) for the package.
<!-- markdownlint-enable MD034 -->

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

We welcome contributions from anyone in the community. Please look at the [Contributing instructions](https://github.com/bryanwweber/thermostate/blob/master/CONTRIBUTING.md) for more information. This project follows the [Contributor Covenant Code of Conduct](https://github.com/bryanwweber/thermostate/blob/master/CODE_OF_CONDUCT.md), version 1.4. In short, be excellent to each other.

## Continuous Integration Status

TravisCI: [![Build Status](https://travis-ci.org/bryanwweber/thermostate.svg?branch=master)](https://travis-ci.org/bryanwweber/thermostate)
Appveyor: [![Build status](https://ci.appveyor.com/api/projects/status/my7m8k82udbkts9h/branch/master?svg=true)](https://ci.appveyor.com/project/bryanwweber/thermostate/branch/master)
[![codecov](https://codecov.io/gh/bryanwweber/thermostate/branch/master/graph/badge.svg)](https://codecov.io/gh/bryanwweber/thermostate)

## Anaconda Package Version

[![Anaconda-Server Badge Version](https://anaconda.org/bryanwweber/thermostate/badges/version.svg)](https://anaconda.org/bryanwweber/thermostate)
[![Anaconda-Server Badge Downloads](https://anaconda.org/bryanwweber/thermostate/badges/downloads.svg)](https://anaconda.org/bryanwweber/thermostate)
