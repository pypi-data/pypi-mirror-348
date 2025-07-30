Contributing to grogupy
=======================

Currently there is no way to contribute to the development.
However here is a summary for the 'approved' developers.

Create environment
------------------

First you have to clone the repository from Github.

.. code-block:: bash

    git clone https://github.com/danielpozsar/grogu.git

Then the easiest way is to create a a virtual environment (.venv), for
example with VSCode.

* Use at least python 3.9

* install dependencies from:

  * requirements.txt

  * requirements-dev.txt

  * /docs/requirements.txt

Finally you have to install and run ``pre-commit``, which is mainly used
to automatically format the code, which makes it nicer and reduces git
differences.

.. code-block:: bash

    pre-commit install
    pre-commit run --all-files



Build and upload wheel
----------------------

You can find a detailed documentation on `PYPI <https://packaging.python.
org/en/latest/tutorials/packaging-projects/>`_, but you can read here a
short summary. First you need some API Tokens for PyPi, to be able
to upload. You can read about this `here 
<https://test.pypi.org/help/#apitoken>`_. I own the current project, so you 
have to contact me.

Use the following commands for a quick setup from the **grogupy_project**
folder:

* Build wheel.

.. code-block:: bash

    python -m build

* Install wheel.

.. code-block:: bash

    pip install dist/grogupy<version>

* Run tests.

.. code-block:: bash

    pytest

If you want to upload to the PYPI repository, then don't forget to 
rewrite the version numbers.

.. code-block:: bash

    python -m twine upload dist/*

Build documentation
-------------------

Yo can go to the **docs/source** directory and modify the *.rst*
files to change the documentation. However to document the API of the
package it is advised to use automatic documentation generation.

* To build the documentation navigate to the **docs/source** folder.

.. code-block:: bash

    cd docs/source

* Then build the documentation. After this the html page can be found in
  **docs/source/_build/html**. If there is already a documentation you can
  remove it by running ``make clean``.

.. code-block:: bash

    make html
