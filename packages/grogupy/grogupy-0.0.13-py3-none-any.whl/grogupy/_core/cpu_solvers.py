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

import numpy as np

from .._tqdm import _tqdm
from ..config import CONFIG
from ..physics.utilities import interaction_energy, second_order_energy
from .utilities import calc_Vu, onsite_projection, parallel_Gk, sequential_Gk, tau_u


def solve_parallel_over_k(builder: "Builder", print_memory: bool = False) -> None:
    """It calculates the energies by the Greens function method.

    It inverts the Hamiltonians of all directions set up in the given
    k-points at the given energy levels. The solution is parallelized over
    k-points. It uses the `greens_function_solver` instance variable which
    controls the solution method over the energy samples. Generally this is
    the fastest solution method for a smaller number of nodes.

    Parameters
    ----------
    builder: Builder
        The main grogupy object
    print_memory: bool, optional
        It can be turned on to print extra memory info, by default False
    """

    # initialize MPI
    from mpi4py import MPI

    comm = MPI.COMM_WORLD
    parallel_size = CONFIG.parallel_size
    root_node = 0
    rank = comm.Get_rank()

    # reset hamiltonians, magnetic entities and pairs
    builder._rotated_hamiltonians = []
    for mag_ent in builder.magnetic_entities:
        mag_ent.reset()
        mag_ent.energies = []
    for pair in builder.pairs:
        pair.reset()
        pair.energies = []

    # iterate over the reference directions (quantization axes)
    for i, orient in enumerate(builder.ref_xcf_orientations):
        # split k points to parallelize
        # (this could be outside loop, but it was an easy fix for the
        # reset of tqdm in each reference direction)
        parallel_k = np.array_split(builder.kspace.kpoints, parallel_size)
        parallel_w = np.array_split(builder.kspace.weights, parallel_size)

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

        mag_ent_mem = 0
        # setup empty Greens function holders for integration
        for mag_ent in _tqdm(
            builder.magnetic_entities,
            desc="Setup magnetic entities for rotated hamiltonian",
        ):
            mag_ent._Gii_tmp = np.zeros(
                (builder.contour.eset, mag_ent.SBS, mag_ent.SBS),
                dtype="complex128",
            )
            mag_ent_mem += sys.getsizeof(mag_ent._Gii_tmp)

        pair_mem = 0
        for pair in _tqdm(builder.pairs, desc="Setup pairs for rotated hamiltonian"):
            pair._Gij_tmp = np.zeros(
                (builder.contour.eset, pair.SBS1, pair.SBS2), dtype="complex128"
            )
            pair._Gji_tmp = np.zeros(
                (builder.contour.eset, pair.SBS2, pair.SBS1), dtype="complex128"
            )
            pair_mem += sys.getsizeof(pair._Gij_tmp) + sys.getsizeof(pair._Gji_tmp)

        if rank == root_node:
            parallel_k[rank] = _tqdm(
                parallel_k[rank], desc=f"Rotation {i+1}, parallel over k on CPU{rank}"
            )

            if print_memory:
                print("\n\n\n")
                print(
                    "################################################################################"
                )
                print(
                    "################################################################################"
                )
                print("Memory allocated on each MPI rank:")
                print(f"Memory allocated by rotated Hamilonian: {rot_H_mem/1e6} MB")
                print(f"Memory allocated by magnetic entities: {mag_ent_mem/1e6} MB")
                print(f"Memory allocated by pairs: {pair_mem/1e6} MB")
                print(
                    f"Total memory allocated in RAM: {(rot_H_mem+mag_ent_mem+pair_mem)/1e6} MB"
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
                    G_mem = builder.hamiltonian.NO * builder.hamiltonian.NO * 16
                else:
                    raise Exception("Unknown Greens function solver!")

                print(f"Memory allocated for Greens function samples: {G_mem/1e6} MB")
                print(
                    f"Total peak memory during solution: {(rot_H_mem+mag_ent_mem+pair_mem+G_mem)/1e6} MB"
                )
                print(
                    "################################################################################"
                )
                print(
                    "################################################################################"
                )
                print("\n\n\n")
        # sampling the integrand on the contour and the BZ
        for j, k in enumerate(parallel_k[rank]):
            # weight of k point in BZ integral
            wk: float = parallel_w[rank][j]

            # calculate Hamiltonian and Overlap matrix in a given k point
            Hk, Sk = rot_H.HkSk(k)

            if builder.greens_function_solver[0].lower() == "p":  # parallel solver
                Gk = parallel_Gk(
                    Hk,
                    Sk,
                    builder.contour.samples,
                    builder.contour.eset,
                )
            elif builder.greens_function_solver[0].lower() == "s":  # sequential solver
                # solve Greens function sequentially for the energies, because of memory bound
                Gk = sequential_Gk(
                    Hk,
                    Sk,
                    builder.contour.samples,
                    builder.contour.eset,
                )

            # store the Greens function slice of the magnetic entities
            for mag_ent in builder.magnetic_entities:
                mag_ent._Gii_tmp += (
                    onsite_projection(
                        Gk, mag_ent._spin_box_indices, mag_ent._spin_box_indices
                    )
                    * wk
                )

            for pair in builder.pairs:
                # add phase shift based on the cell difference
                phase: NDArray = np.exp(1j * 2 * np.pi * k @ pair.supercell_shift.T)

                # store the Greens function slice of the pairs
                pair._Gij_tmp += (
                    onsite_projection(Gk, pair.SBI1, pair.SBI2) * phase * wk
                )
                pair._Gji_tmp += (
                    onsite_projection(Gk, pair.SBI2, pair.SBI1) / phase * wk
                )

        # sum reduce partial results of mpi nodes and delete temprorary stuff
        for mag_ent in builder.magnetic_entities:
            # initialize rotation storage
            mag_ent._Vu1_tmp = []
            mag_ent._Vu2_tmp = []

            mag_ent._Gii_reduce = np.zeros(
                (builder.contour.eset, mag_ent.SBS, mag_ent.SBS),
                dtype="complex128",
            )
            comm.Reduce(mag_ent._Gii_tmp, mag_ent._Gii_reduce, root=root_node)
            del mag_ent._Gii_tmp

        for pair in builder.pairs:
            pair._Gij_reduce = np.zeros(
                (builder.contour.eset, pair.SBS1, pair.SBS2), dtype="complex128"
            )
            pair._Gji_reduce = np.zeros(
                (builder.contour.eset, pair.SBS2, pair.SBS1), dtype="complex128"
            )
            comm.Reduce(pair._Gij_tmp, pair._Gij_reduce, root=root_node)
            comm.Reduce(pair._Gji_tmp, pair._Gji_reduce, root=root_node)
            del pair._Gij_tmp
            del pair._Gji_tmp

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
                        interaction_energy(Vui, Vuj, Gij, Gji, builder.contour.weights)
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
            rot_H.rotate(rot_H.scf_xcf_orientation)
            for mag_ent in builder.magnetic_entities:
                mag_ent._Vu1.append([])
                mag_ent._Vu2.append([])
                mag_ent._Gii.append([])
            for pair in builder.pairs:
                pair._Gij.append([])
                pair._Gji.append([])

    # finalize energies of the magnetic entities and pairs
    # calculate magnetic parameters
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


if __name__ == "__main__":
    pass
