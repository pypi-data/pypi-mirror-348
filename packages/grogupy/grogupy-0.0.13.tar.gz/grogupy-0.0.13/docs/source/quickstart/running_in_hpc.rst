.. _running_in_hpc:

Running grogupy in HPC
======================
This section provides instructions on how to configure and run grogupy on a 
High-Performance Computing (HPC) system using SLURM. Below is an example of a 
bash script for submitting a job to the SLURM scheduler.

Example SLURM batch script
---------------------------

The following is an example SLURM batch script (`sbatch`) for running grogupy 
on an HPC system, in this case on `Komondor 
<https://hpc.kifu.hu/hu/komondor.html>`_:

.. code-block:: bash

    #!/bin/bash
    #SBATCH --job-name=grogupy
    #SBATCH --nodes=1
    #SBATCH --ntasks=1
    #SBATCH --ntasks-per-node=1
    #SBATCH --cpus-per-task=128
    #SBATCH --time=01:00:00
    #SBATCH --gres=gpu:8
    #SBATCH --partition=ai
    #SBATCH --exclusive
    #SBATCH --mem-per-cpu 4000

    ulimit -s unlimited

    source ~/.bashrc
    yes | module clear
    module purge
    module load PrgEnv-gnu cray-pals cray-python cuda/12.3

    export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
    export OPENBLAS_NUM_THREADS=$SLURM_CPUS_PER_TASK
    export MKL_NUM_THREADS=$SLURM_CPUS_PER_TASK
    export VECLIB_MAXIMUM_THREADS=$SLURM_CPUS_PER_TASK
    export NUMEXPR_NUM_THREADS=$SLURM_CPUS_PER_TASK

    export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/software/packages/cuda/12.3/targets/x86_64-linux/lib
    export grogupy_ARCHITECTURE=GPU

    time srun grogupy_run ./grogupy_input.py

Explanation of the script
-------------------------

- `#SBATCH --job-name=grogupy`: Sets the name of the job.
- `#SBATCH --nodes=1`: Requests one node.
- `#SBATCH --ntasks=1`: Requests one task.
- `#SBATCH --ntasks-per-node=1`: Specifies one task per node.
- `#SBATCH --cpus-per-task=128`: Allocates 128 CPUs per task.
- `#SBATCH --time=01:00:00`: Sets a time limit of 1 hours for the job.
- `#SBATCH --gres=gpu:8`: Requests 8 GPUs.
- `#SBATCH --partition=ai`: Specifies the partition to submit the job to.
- `#SBATCH --exclusive`: Ensures exclusive access to the node.
- `#SBATCH --mem-per-cpu 4000`: Allocates 4000 MB of memory per CPU.

The script also sets up the environment by loading necessary
modules and setting environment variables for optimal
performance. Exportin the LD_LIBRARY_PATH variable is necessary
to ensure that the CUDA library is accessible for cupy. The
script also sets the `grogupy_ARCHITECTURE` environment
variable to `GPU` to enable GPU acceleration in grogupy.
Finally, it runs the grogupy application using `srun` and the
`grogupy` command line script.

Make sure to adjust the script parameters according to
your HPC system's configuration and your specific requirements.


Example input file format
-------------------------

This is the corresponding input file for the above script, `grogupy_input.py`,
which contains the parameters for the grogupy simulation. These variables
are passed to the appropriate functions in the grogupy package very similarly
as we did in the jupyter notebook examples.

.. code-block:: python

   # Copyright (c) [2024-2025] [Laszlo Oroszlany, Daniel Pozsar]
   #
   # Permission is hereby granted, free of charge, to any person obtaining a copy
   # of this software and associated documentation files (the "Software"), to deal
   # in the Software without restriction, including without limitation the rights
   # to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
   # copies of the Software, and to permit persons to whom the Software is
   # furnished to do so, subject to the following conditions:
   #
   # The above copyright notice and this permission notice shall be included in all
   # copies or substantial portions of the Software.
   #
   # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
   # IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
   # FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
   # AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
   # LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
   # OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
   # SOFTWARE.


   ###############################################################################
   #                                 Input files
   ###############################################################################


   infolder = "./benchmarks/CrI3"
   infile = "CrI3.fdf"


   ###############################################################################
   #                            Convergence parameters
   ###############################################################################


   # kset should be at leas 100x100 for 2D diatomic systems
   kset = [2, 2, 1]
   # eset should be 100 for insulators and 1000 for metals
   eset = 100
   # esetp should be 600 for insulators and 10000 for metals
   esetp = 600
   # emin None sets the minimum energy to the minimum energy in the eigfile
   emin = None
   # emax is at the Fermi level at 0
   emax = 0
   # the bottom of the energy contour should be shifted by -5 eV
   emin_shift = -5
   # the top of the energy contour can be shifted to the middle of the gap for
   # insulators
   emax_shift = 0


   ###############################################################################
   #                                 Orientations
   ###############################################################################


   # usually the DFT calculation axis is [0, 0, 1]
   scf_xcf_orientation = [0, 0, 1]
   # the reference directions for the energy derivations
   ref_xcf_orientations = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]


   ###############################################################################
   #                      Magnetic entity and pair definitions
   ###############################################################################


   # magnetic entities and pairs can be defined automatically from the cutoff
   # radius and magnetic atoms
   setup_from_range = True
   radius = 20
   atomic_subset = "Cr"
   kwargs_for_mag_ent = dict(l=2)


   ###############################################################################
   #                                Memory management
   ###############################################################################


   # maximum number of pairs per loop, reduce it to avoid memory overflow
   max_pairs_per_loop = 10000
   # in low memory mode we discard some temporary data that could be useful for
   # interactive work
   low_memory_mode = True
   # sequential solver is better for large systems
   greens_function_solver = "Parallel"
   # maximum number of greens function samples per loop, when 
   # greens_function_solver is set to "Sequential", reduce it to avoid memory 
   # overflow on GPU for large systems
   max_g_per_loop = 20


   ###############################################################################
   #                                 Solution methods
   ###############################################################################


   # the calculation of J and K from the energy derivations, either Fit or Grogupy
   exchange_solver = "Fit"
   anisotropy_solver = "Fit"


   ###############################################################################
   #                                   Output files
   ###############################################################################


   # either total or local, which controls if only the magnetic
   # entity's magnetic monent or the whole atom's magnetic moment is printed
   # used by all output modes
   out_magnetic_moment = "Total"

   # save the magnopy file
   save_magnopy = True
   # precision of numerical values in the magnopy file
   magnopy_precision = None
   # add the simulation parameters to the magnopy file as comments
   magnopy_comments = True

   # save the Uppsala Atomistic Spin Dynamics software input files
   # uses the outfolder and out_magentic_moment
   save_UppASD = True
   # add the simulation parameters to the cell.tmp.txt file as 
   # comments
   uppasd_comments = True

   # save the pickle file
   save_pickle = True
   """
   The compression level can be set to 0,1,2. Every other value defaults to 2.
   0. This means that there is no compression at all.

   1. This means, that the keys "_dh" and "_ds" are set
   to None, because othervise the loading would be dependent
   on the sisl version

   2. This contains compression 1, but sets the keys "Gii",
   "Gij", "Gji", "Vu1" and "Vu2" to [], to save space
   """
   pickle_compress_level = 2

   # output folder, for example the current folder
   outfolder = "./src/grogupy/cli/tests/"
   # outfile name
   outfile = "test"


   ###############################################################################
   ###############################################################################