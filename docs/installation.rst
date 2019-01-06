============
Installation
============

Conda
-----

The preferred installation method is to use `conda <https://anaconda.com/download>`__.
Using Conda, ThermoState can be installed for either Python 3.5, 3.6, or 3.7. If you have an existing
Conda environment with one of those Python versions, installing ThermoState can be done by

.. code-block:: bash

   conda install -c bryanwweber thermostate conda-forge::pint


This installs Pint from the ``conda-forge`` channel; if you would like to use another channel to
install Pint, change the ``conda-forge`` to be the name of the channel you prefer. If Pint is
already installed in your environment, the ``conda-forge::pint`` can be omitted entirely.

If you do not have an environment with Python 3.5, 3.6, or 3.7, you can create a new environment
with

.. code-block:: bash

   conda create -n thermostate -c bryanwweber thermostate conda-forge::pint

Pip
---

Alternatively, ThermoState can be installed with pip.

.. code-block:: bash

   pip install thermostate

From Source
-----------

ThermoState is a pure-Python package that supports any Python version 3.5 and higher.
To install from source, clone the source code repository and install using ``pip``.

.. code-block:: bash

   git clone https://github.com/bryanwweber/thermostate
   cd thermostate
   pip install .
