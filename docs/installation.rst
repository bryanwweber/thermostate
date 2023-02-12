============
Installation
============

Conda
-----

The preferred installation method is to use `conda <https://anaconda.com/download>`__. Using Conda, ThermoState can be installed for Python 3.9 and up. You can create a new environment with:

.. code-block:: bash

   conda create -n thermostate -c conda-forge thermostate

Pip
---

Alternatively, ThermoState can be installed with pip.

.. code-block:: bash

   python -m pip install thermostate

From Source
-----------

ThermoState is a pure-Python package that supports any Python version 3.9 and higher.
To install from source, clone the source code repository and install using ``pip``.

.. code-block:: bash

   git clone https://github.com/bryanwweber/thermostate
   cd thermostate
   python -m pip install .
