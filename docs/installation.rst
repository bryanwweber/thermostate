============
Installation
============

Conda
-----

The preferred installation method is to use `conda <https://anaconda.com/download>`__.
Using Conda, ThermoState can be installed for either Python 3.5 or 3.6. If you have an existing
Conda environment with one of those Python versions, installing ThermoState can be done by

.. code-block:: bash

   conda install -c bryanwweber thermostate conda-forge::pint


This installs Pint from the ``conda-forge`` channel; if you would like to use another channel to
install Pint, or Pint is already installed in your environment, the ``conda-forge::pint`` can be
omitted.

If you do not have an environment with Python 3.5 or 3.6, you can create a new environment with

.. code-block:: bash

   conda create -n thermostate -c bryanwweber thermostate conda-forge::pint

Pip
---

Alternatively, ThermoState can be installed with pip, for Python 3.5 only. This is because version
6.1.0 of CoolProp is only available for Python 3.5 from pip.

.. code-block:: bash

   pip install thermostate

From Source
-----------

ThermoState is a pure-Python package that supports any Python version 3.5 and higher. Binary
installers for CoolProp (which has a C-extension for its Python interface) are only available for
Python 3.5 (pip) and Pythons 3.5 and 3.6 (Conda). Other versions of Python can be supported by
compiling CoolProp locally, for which instructions are available on the
`CoolProp documentation <http://www.coolprop.org/dev/coolprop/wrappers/Python/index.html#manual-installation>`__.
Once CoolProp is installed, installing ThermoState can be done by

.. code-block:: bash

   git clone https://github.com/bryanwweber/thermostate
   cd thermostate
   pip install .
