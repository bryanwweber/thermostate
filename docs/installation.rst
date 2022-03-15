============
Installation
============

Conda
-----

The preferred installation method is to use `conda <https://anaconda.com/download>`__.
Using Conda, ThermoState can be installed for Python 3.7 and up. If you have an existing
Conda environment with one of those Python versions, installing ThermoState can be done by:

.. code-block:: bash

   conda install -c conda-forge thermostate


This installs ThermoState and its dependencies from the ``conda-forge`` channel.

If you do not have an environment with Python 3.7 or higher you can create a new environment
with:

.. code-block:: bash

   conda create -n thermostate -c conda-forge thermostate

Pip
---

Alternatively, ThermoState can be installed with pip.

.. code-block:: bash

   python -m pip install thermostate

Note that for versions of Python >= 3.9, CoolProp 6.4.1 will not work from PyPI. You'll
need to install CoolProp from their source repository until CoolProp >6.4.1 is
released. In this case, you can still install ThermoState from PyPI by specifying
not to install the dependencies automatically:

.. code-block:: bash

   python -m pip install --no-deps thermostate matplotlib numpy pint

Then you'll need to install CoolProp into the same environment separately. Note that
the conda package is available for all Python versions after 3.7.

From Source
-----------

ThermoState is a pure-Python package that supports any Python version 3.7 and higher.
To install from source, clone the source code repository and install using ``pip``.

.. code-block:: bash

   git clone https://github.com/bryanwweber/thermostate
   cd thermostate
   python -m pip install .
