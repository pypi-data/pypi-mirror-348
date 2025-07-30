# Copyright (c) [2024-2025] [Grogupy Team]
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
from typing import TYPE_CHECKING

from numpy.typing import NDArray

if TYPE_CHECKING:
    from ..physics.builder import Builder

import sys
from concurrent.futures import ThreadPoolExecutor

import numpy as np

from .._tqdm import _tqdm
from ..config import CONFIG
from ..physics.utilities import interaction_energy, second_order_energy
from .utilities import calc_Vu, onsite_projection, tau_u

if CONFIG.is_GPU:
    # initialize parallel GPU stuff
    import cupy as cp
    from cupy.typing import NDArray as CNDArray

    # Disable memory pool for device memory (GPU)
    cp.cuda.set_allocator(None)
    # Disable memory pool for pinned memory (CPU).
    cp.cuda.set_pinned_memory_allocator(None)

    def gpu_solver(
        max_g_per_loop: int,
        mode: str,
        gpu_number: int,
        kpoints: list[NDArray],
        kweights: list[NDArray],
        SBI: list[NDArray],
        SBI1: list[NDArray],
        SBI2: list[NDArray],
        Ruc: list[NDArray],
        sc_off: NDArray,
        samples: NDArray,
        G_mag: list[NDArray],
        G_pair_ij: list[NDArray],
        G_pair_ji: list[NDArray],
        rotated_H: list[NDArray],
        S: NDArray,
        rot_num: str = "Unknown",
    ) -> tuple["CNDArray", "CNDArray", "CNDArray"]:
        """Parallelizes the Green's function solution on GPU.

        Should be used on large systems.

        Parameters
        ----------
        max_g_per_loop: int
            Maximum number of greens function samples per loop
        mode : str
            The Greens function solver, which can be parallel or sequential
        gpu_number : int
            The ID of the GPU which we want to run on
        kpoints : list[NDArray]
            The kpoints already split for the GPUs
        kweights : list[NDArray]
            The kpoint weights already split for the GPUs
        SBI : list[NDArray]
            Spin box indices for the magnetic entities
        SBI1 : list[NDArray]
            Spin box indices for the pairs
        SBI2 : list[NDArray]
            Spin box indices for the pairs
        Ruc : list[NDArray]
            Unit cell shift of the pairs
        sc_off : NDArray
            List of unit cell shifts for unit cell indexes
        samples : NDArray
            Energy samples
        G_mag : list[NDArray]
            Empty container for the final Green's function on each magnetic entity
        G_pair_ij : list[NDArray]
            Empty container for the final Green's function on each pair
        G_pair_ji : list[NDArray]
            Empty container for the final Green's function on each pair
        rotated_H : list[NDArray]
            Hamiltonian with rotated exchange field
        S : NDArray
            Overlap matrix, should be the same for all Hamiltonians
        rot_num: str, optional
            Rotation number for tqdm print, by default "Unknown"

        Returns
        -------
        local_G_mag : CNDArray
            The Greens function of the mangetic entities
        local_G_pair_ij : CNDArray
            The Greens function from mangetic entity i to j on the given GPU
        local_G_pair_ji : CNDArray
            The Greens function from mangetic entity j to i on the given GPU
        """

        # use the specified GPU
        with cp.cuda.Device(gpu_number):
            # copy everything to GPU
            local_kpoints = cp.array(kpoints[gpu_number])
            local_kweights = cp.array(kweights[gpu_number])
            local_SBI = cp.array(SBI)
            local_SBI1 = cp.array(SBI1)
            local_SBI2 = cp.array(SBI2)
            local_Ruc = cp.array(Ruc)

            local_sc_off = cp.array(sc_off)
            eset = samples.shape[0]
            local_samples = cp.array(samples.reshape(eset, 1, 1))

            local_G_mag = np.zeros_like(G_mag)
            local_G_pair_ij = np.zeros_like(G_pair_ij)
            local_G_pair_ji = np.zeros_like(G_pair_ji)

            for i in _tqdm(
                range(len(local_kpoints)),
                desc=f"Rotation {rot_num}, parallel over k on GPU{gpu_number+1}",
            ):
                # weight of k point in BZ integral
                wk = local_kweights[i]
                k = local_kpoints[i]

                # calculate Hamiltonian and Overlap matrix in a given k point
                # this generates the list of phases
                phases = cp.exp(-1j * 2 * cp.pi * k @ local_sc_off.T)
                # phases applied to the hamiltonian
                HK = cp.einsum("abc,a->bc", cp.array(rotated_H), phases)
                SK = cp.einsum("abc,a->bc", cp.array(S), phases)

                # solve the Greens function on all energy points separately
                if mode == "sequential":
                    # make chunks for reduced parallelization over energy sample points
                    number_of_chunks = np.floor(eset / max_g_per_loop) + 1

                    # constrain to sensible size
                    if number_of_chunks > eset:
                        number_of_chunks = eset

                    # create batches using slices on every instance
                    slices = np.array_split(range(eset), number_of_chunks)

                    # fills the holders sequentially by the Greens function slices on
                    # a given energy
                    for slice in slices:
                        Gk = cp.linalg.inv(SK * local_samples[slice] - HK)

                        # store the Greens function slice of the magnetic entities
                        for l, sbi in enumerate(local_SBI):
                            local_G_mag[l][slice] += (
                                Gk[..., sbi, :][..., sbi] * wk
                            ).get()

                        # store the Greens function slice of the pairs
                        for l, dat in enumerate(zip(local_SBI1, local_SBI2, local_Ruc)):
                            sbi1, sbi2, ruc = dat
                            phase = cp.exp(1j * 2 * cp.pi * k @ ruc.T)

                            local_G_pair_ij[l][slice] += (
                                Gk[..., sbi1, :][..., sbi2] * wk * phase
                            ).get()
                            local_G_pair_ji[l][slice] += (
                                Gk[..., sbi2, :][..., sbi1] * wk / phase
                            ).get()

                # solve the Greens function on all energy points in one step
                elif mode == "parallel":
                    Gk = cp.linalg.inv(SK * local_samples - HK)

                    # store the Greens function slice of the magnetic entities
                    for l, sbi in enumerate(local_SBI):
                        local_G_mag[l] += (Gk[..., sbi, :][..., sbi] * wk).get()

                    # store the Greens function slice of the pairs
                    for l, dat in enumerate(zip(local_SBI1, local_SBI2, local_Ruc)):
                        sbi1, sbi2, ruc = dat
                        phase = cp.exp(1j * 2 * cp.pi * k @ ruc.T)

                        local_G_pair_ij[l] += (
                            Gk[..., sbi1, :][..., sbi2] * wk * phase
                        ).get()
                        local_G_pair_ji[l] += (
                            Gk[..., sbi2, :][..., sbi1] * wk / phase
                        ).get()

            # release them from memory
            local_kpoints = None
            local_kweights = None
            local_SBI = None
            local_SBI1 = None
            local_SBI2 = None
            local_Ruc = None
            local_sc_off = None
            eset = None
            local_samples = None
            Gk = None
            HK = None
            SK = None
            phase = None
            phases = None
        return local_G_mag, local_G_pair_ij, local_G_pair_ji

    def solve_parallel_over_k(builder: "Builder", print_memory: bool = False) -> None:
        """It calculates the energies by the Greens function method.

        It inverts the Hamiltonians of all directions set up in the given
        k-points at the given energy levels. The solution is parallelized over
        k-points. It uses the number of GPUs given. And determines the parallelization
        over energy levels from the ``builder.greens_function_solver`` attribute.

        Parameters
        ----------
        builder : Builder
            The system that we want to solve
        print_memory: bool, optional
            It can be turned on to print extra memory info, by default False
        """

        parallel_size = CONFIG.parallel_size

        # split k points to parallelize
        parallel_k = np.array_split(builder.kspace.kpoints, parallel_size)
        parallel_w = np.array_split(builder.kspace.weights, parallel_size)

        # reset hamiltonians, magnetic entities and pairs
        builder._rotated_hamiltonians = []
        for mag_ent in builder.magnetic_entities:
            mag_ent.reset()
            mag_ent.energies = []
        for pair in builder.pairs:
            pair.reset()
            pair.energies = []

        # iterate over the reference directions (quantization axes)
        for rot_num, orient in enumerate(builder.ref_xcf_orientations):
            # empty greens functions holders
            G_mag_reduce = []
            G_pair_ij_reduce = []
            G_pair_ji_reduce = []

            # obtain rotated exchange field and Hamiltonian
            if builder.low_memory_mode:
                rot_H = builder.hamiltonian
            else:
                rot_H = builder.hamiltonian.copy()
            rot_H.rotate(orient["o"])
            rot_H_mem = np.sum(
                [
                    sys.getsizeof(rot_H.H),
                    sys.getsizeof(rot_H.S),
                ]
            )

            # setup empty Greens function holders for integration
            for mag_ent in _tqdm(
                builder.magnetic_entities,
                desc="Setup magnetic entities for rotated hamiltonian",
            ):
                G_mag_reduce.append(
                    np.zeros(
                        (builder.contour.eset, mag_ent.SBS, mag_ent.SBS),
                        dtype="complex128",
                    )
                )

            for pair in _tqdm(
                builder.pairs, desc="Setup pairs for rotated hamiltonian"
            ):
                G_pair_ij_reduce.append(
                    np.zeros(
                        (builder.contour.eset, pair.SBS1, pair.SBS2), dtype="complex128"
                    )
                )
                G_pair_ji_reduce.append(
                    np.zeros(
                        (builder.contour.eset, pair.SBS2, pair.SBS1), dtype="complex128"
                    )
                )

            # convert everything so it can be passed to the GPU solvers
            G_mag_reduce = np.array(G_mag_reduce)
            mag_ent_mem = sys.getsizeof(G_mag_reduce)
            G_pair_ij_reduce = np.array(G_pair_ij_reduce)
            G_pair_ji_reduce = np.array(G_pair_ji_reduce)
            pair_mem = sys.getsizeof(G_pair_ij_reduce) + sys.getsizeof(G_pair_ji_reduce)

            SBI = [m._spin_box_indices for m in builder.magnetic_entities]
            SBI1 = [p.SBI1 for p in builder.pairs]
            SBI2 = [p.SBI2 for p in builder.pairs]
            Ruc = [p.supercell_shift for p in builder.pairs]

            S = builder.hamiltonian.S
            H = builder.hamiltonian.H

            sc_off = builder.hamiltonian.sc_off
            samples = builder.contour.samples

            if print_memory:
                print("\n\n\n")
                print(
                    "################################################################################"
                )
                print(
                    "################################################################################"
                )
                print(f"Memory allocated by rotated Hamilonian: {rot_H_mem/1e6} MB")
                print(f"Memory allocated by magnetic entities: {mag_ent_mem/1e6} MB")
                print(f"Memory allocated by pairs: {pair_mem/1e6} MB")
                print(
                    f"Total memory allocated in RAM: {(rot_H_mem+mag_ent_mem+pair_mem) / 1e6} MB"
                )
                print(
                    "--------------------------------------------------------------------------------"
                )
                if builder.greens_function_solver[0].lower() == "p":  # parallel solver
                    # 16 is the size of complex numbers in byte, when using np.float64
                    G_mem = (
                        builder.contour.eset
                        * builder.hamiltonian.NO
                        * builder.hamiltonian.NO
                        * 16
                    )
                elif (
                    builder.greens_function_solver[0].lower() == "s"
                ):  # sequentia solver
                    G_mem = (
                        builder.max_g_per_loop
                        * builder.hamiltonian.NO
                        * builder.hamiltonian.NO
                        * 16
                    )
                else:
                    raise Exception("Unknown Greens function solver!")

                print("Memory allocated on GPU:")
                print(f"Memory allocated by rotated Hamilonian: {rot_H_mem/1e6} MB")
                print(f"Memory allocated for Greens function samples: {G_mem/1e6} MB")
                # 25 is the maximum amount of memory used for matrix inversion
                gpu_max_mem = (
                    np.max([mag_ent_mem + pair_mem + rot_H_mem, G_mem * 25]) / 1e6
                )
                print(f"Total peak memory on GPU during solution: {gpu_max_mem} MB")
                print(
                    "################################################################################"
                )
                print(
                    "################################################################################"
                )
                print("\n\n\n")

            # call the solvers
            if builder.greens_function_solver[0].lower() == "p":  # parallel solver
                mode = "parallel"
            elif builder.greens_function_solver[0].lower() == "s":  # sequential solver
                mode = "sequential"
            else:
                raise Exception("Unknown Green's function solver!")

            with ThreadPoolExecutor(max_workers=parallel_size) as executor:
                futures = [
                    executor.submit(
                        gpu_solver,
                        builder.max_g_per_loop,
                        mode,
                        gpu_number,
                        parallel_k,
                        parallel_w,
                        SBI,
                        SBI1,
                        SBI2,
                        Ruc,
                        sc_off,
                        samples,
                        G_mag_reduce,
                        G_pair_ij_reduce,
                        G_pair_ji_reduce,
                        H,
                        S,
                        rot_num + 1,
                    )
                    for gpu_number in range(parallel_size)
                ]
                results = [future.result() for future in futures]

            # Combine results
            for G_mag_local, G_pair_ij_local, G_pair_ji_local in results:
                G_mag_reduce += G_mag_local.get()
                G_pair_ij_reduce += G_pair_ij_local.get()
                G_pair_ji_reduce += G_pair_ji_local.get()

            # release them from memory
            results = None

            for i, mag_ent in enumerate(builder.magnetic_entities):
                # initialize rotation storage
                mag_ent._Vu1_tmp = []
                mag_ent._Vu2_tmp = []

                mag_ent._Gii_reduce = G_mag_reduce[i]

            for i, pair in enumerate(builder.pairs):
                pair._Gij_reduce = G_pair_ij_reduce[i]
                pair._Gji_reduce = G_pair_ji_reduce[i]

            # these are the rotations mostly perpendicular to the quantization axis
            for u in orient["vw"]:
                # section 2.H
                _, _, _, H_XCF = rot_H.extract_exchange_field()
                Tu: NDArray = np.kron(
                    np.eye(int(builder.hamiltonian.NO / 2), dtype=int), tau_u(u)
                )
                Vu1, Vu2 = calc_Vu(H_XCF[rot_H.uc_in_sc_index], Tu)

                for mag_ent in _tqdm(
                    builder.magnetic_entities,
                    desc="Setup perturbations for rotated hamiltonian",
                ):
                    # fill up the perturbed potentials (for now) based on the on-site projections
                    mag_ent._Vu1_tmp.append(
                        onsite_projection(
                            Vu1, mag_ent._spin_box_indices, mag_ent._spin_box_indices
                        )
                    )
                    mag_ent._Vu2_tmp.append(
                        onsite_projection(
                            Vu2, mag_ent._spin_box_indices, mag_ent._spin_box_indices
                        )
                    )

            # calculate energies in the current reference hamiltonian direction
            for mag_ent in builder.magnetic_entities:
                storage: list[float] = []
                # iterate over the first and second order local perturbations
                Gii = mag_ent._Gii_reduce
                V1 = mag_ent._Vu1_tmp
                V2 = mag_ent._Vu2_tmp

                # fill up the magnetic entities list with the energies
                storage.append(
                    second_order_energy(V1[0], V2[0], Gii, builder.contour.weights)
                )
                storage.append(
                    interaction_energy(V1[0], V1[1], Gii, Gii, builder.contour.weights)
                )
                storage.append(
                    interaction_energy(V1[1], V1[0], Gii, Gii, builder.contour.weights)
                )
                storage.append(
                    second_order_energy(V1[1], V2[1], Gii, builder.contour.weights)
                )
                if builder.anisotropy_solver.lower()[0] == "g":  # grogupy
                    storage.append(
                        second_order_energy(V1[2], V2[2], Gii, builder.contour.weights)
                    )
                mag_ent.energies.append(storage)

            # calculate energies in the current reference hamiltonian direction
            for pair in builder.pairs:
                Gij, Gji = pair._Gij_reduce, pair._Gji_reduce
                storage: list = []
                # iterate over the first order local perturbations in all possible orientations for the two sites
                # actually all possible orientations without the orientation for the off-diagonal anisotropy
                # that is why we only take the first two of each Vu1
                for Vui in pair.M1._Vu1_tmp[:2]:
                    for Vuj in pair.M2._Vu1_tmp[:2]:
                        storage.append(
                            interaction_energy(
                                Vui, Vuj, Gij, Gji, builder.contour.weights
                            )
                        )
                # fill up the pairs dictionary with the energies
                pair.energies.append(storage)

            # if we want to keep all the information for some reason we can do it
            if not builder.low_memory_mode:
                builder._rotated_hamiltonians.append(rot_H)
                for mag_ent in builder.magnetic_entities:
                    mag_ent._Vu1.append(mag_ent._Vu1_tmp)
                    mag_ent._Vu2.append(mag_ent._Vu2_tmp)
                    mag_ent._Gii.append(mag_ent._Gii_reduce)
                for pair in builder.pairs:
                    pair._Gij.append(pair._Gij_reduce)
                    pair._Gji.append(pair._Gji_reduce)
            # or fill with empty stuff
            else:
                for mag_ent in builder.magnetic_entities:
                    mag_ent._Vu1.append([])
                    mag_ent._Vu2.append([])
                    mag_ent._Gii.append([])
                for pair in builder.pairs:
                    pair._Gij.append([])
                    pair._Gji.append([])

        # finalize energies of the magnetic entities and pairs
        # calcualte magnetic parameters
        for mag_ent in builder.magnetic_entities:
            # delete temporary stuff
            del mag_ent._Gii_reduce
            del mag_ent._Vu1_tmp
            del mag_ent._Vu2_tmp

            # convert to NDArray
            mag_ent.energies = np.array(mag_ent.energies)
            # call these so they are updated
            mag_ent.energies_meV
            mag_ent.energies_mRy
            if builder.anisotropy_solver.lower()[0] == "f":  # fit
                mag_ent.fit_anisotropy_tensor(builder.ref_xcf_orientations)
            elif builder.anisotropy_solver.lower()[0] == "g":  # grogupy
                mag_ent.calculate_anisotropy()

        for pair in builder.pairs:
            # delete temporary stuff
            del pair._Gij_reduce
            del pair._Gji_reduce

            # convert to NDArray
            pair.energies = np.array(pair.energies)
            # call these so they are updated
            pair.energies_meV
            pair.energies_mRy
            if builder.exchange_solver.lower()[0] == "f":  # fit
                pair.fit_exchange_tensor(builder.ref_xcf_orientations)
            elif builder.exchange_solver.lower()[0] == "g":  # grogupy
                pair.calculate_exchange_tensor()

else:

    def gpu_solver(
        mode: str,
        gpu_number: int,
        kpoints: list[NDArray],
        kweights: list[NDArray],
        SBI: list[NDArray],
        SBI1: list[NDArray],
        SBI2: list[NDArray],
        Ruc: list[NDArray],
        sc_off: NDArray,
        samples: NDArray,
        G_mag: list[NDArray],
        G_pair_ij: list[NDArray],
        G_pair_ji: list[NDArray],
        rotated_H: list[NDArray],
        S: NDArray,
    ) -> tuple["CNDArray", "CNDArray", "CNDArray"]:
        """Solves the Green's function parallel on GPU.

        Should be used on computation power bound systems.

        Parameters
        ----------
        mode : str
            The Greens function solver, which can be parallel or sequential
        gpu_number : int
            The ID of the GPU which we want to run on
        kpoints : list[NDArray]
            The kpoints already split for the GPUs
        kweights : list[NDArray]
            The kpoint weights already split for the GPUs
        SBI : list[NDArray]
            Spin box indices for the magnetic entities
        SBI1 : list[NDArray]
            Spin box indices for the pairs
        SBI2 : list[NDArray]
            Spin box indices for the pairs
        Ruc : list[NDArray]
            Unit cell shift of the pairs
        sc_off : NDArray
            List of unit cell shifts for unit cell indexes
        samples : NDArray
            Energy samples
        G_mag : list[NDArray]
            Empty container for the final Green's function on each magnetic entity
        G_pair_ij : list[NDArray]
            Empty container for the final Green's function on each pair
        G_pair_ji : list[NDArray]
            Empty container for the final Green's function on each pair
        rotated_H : list[NDArray]
            Hamiltonian with rotated exchange field
        S : NDArray
            Overlap matrix, should be the same for all Hamiltonians

        Returns
        -------
        local_G_mag : CNDArray
            The Greens function of the mangetic entities
        local_G_pair_ij : CNDArray
            The Greens function from mangetic entity i to j on the given GPU
        local_G_pair_ji : CNDArray
            The Greens function from mangetic entity j to i on the given GPU
        """

        raise Exception("GPU is not available!")

    def solve_parallel_over_k(
        builder: "Builder",
    ) -> None:
        """It calculates the energies by the Greens function method.

        It inverts the Hamiltonians of all directions set up in the given
        k-points at the given energy levels. The solution is parallelized over
        k-points. It uses the number of GPUs given. And determines the parallelization
        over energy levels from the ``builder.greens_function_solver`` attribute.

        Parameters
        ----------
        builder : Builder
            The system that we want to solve
        """

        raise Exception("GPU is not available!")


if __name__ == "__main__":
    pass
