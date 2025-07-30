Environment Variables
=====================

Environment variables are key-value pairs that can
affect the way running processes will behave on a computer.

Setting Environment Variables
------------------------------
1. **LD_LIBRARY_PATH**: This variable specifies the directories
   where the system should look for dynamic libraries. For example,
   to ensure that CuPy can find the necessary CUDA libraries, you
   might need to set the `LD_LIBRARY_PATH` as follows:

.. code-block:: bash

    export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/software/packages/cuda/12.3/targets/x86_64-linux/lib

2. **GROGUPY_ARCHITECTURE**: This variable sets the architecture
   for the grogupy project. By default, the architecture is set to
   CPU. To change it to GPU, you can set the `GROGUPY_ARCHITECTURE`
   environment variable:

.. code-block:: bash

    export GROGUPY_ARCHITECTURE=GPU

3. **GROGUPY_TQDM**: With this variable you can request ``tqdm`` for 
   a nice progress bar. It can be set to true of false.

.. code-block:: bash

    export GROGUPY_TQDM=TRUE
