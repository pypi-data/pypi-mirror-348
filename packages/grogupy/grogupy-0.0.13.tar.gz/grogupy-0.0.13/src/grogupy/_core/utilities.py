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
from typing import Any, Union

import numpy as np
import sisl
from numpy.typing import NDArray
from scipy.special import roots_legendre

from .._tqdm import _tqdm
from ..config import CONFIG
from .constants import TAU_X, TAU_Y, TAU_Z

if CONFIG.is_GPU:
    import cupy as cp


def commutator(a: NDArray, b: NDArray) -> NDArray:
    """Shorthand for commutator.

    Commutator of two matrices in the mathematical sense.

    Parameters
    ----------
        a: NDArray
            The first matrix
        b: NDArray
            The second matrix

    Returns
    -------
        NDArray
            The commutator of a and b
    """

    return a @ b - b @ a


def tau_u(u: Union[list, NDArray]) -> NDArray:
    """Pauli matrix in direction u.

    Returns the vector u in the basis of the Pauli matrices.

    Parameters
    ----------
        u: list or NDArray
            The direction

    Returns
    -------
        NDArray
            Arbitrary direction in the base of the Pauli matrices
    """

    # u is force to be of unit length
    u = u / np.linalg.norm(u)

    return u[0] * TAU_X + u[1] * TAU_Y + u[2] * TAU_Z


def crossM(u: Union[list, NDArray]) -> NDArray:
    """Definition for the cross-product matrix.

    It acts as a cross product with vector u.

    Parameters
    ----------
        u: list or NDArray
            The second vector in the cross product

    Returns
    -------
        NDArray
            The matrix that represents teh cross product with a vector
    """

    return np.array([[0, -u[2], u[1]], [u[2], 0, -u[0]], [-u[1], u[0], 0]])


def RotM(theta: float, u: NDArray, eps: float = 1e-10) -> NDArray:
    """Definition of rotation matrix with angle theta around direction u.

    Parameters
    ----------
        theta: float
            The angle of rotation
        u: NDArray
            The rotation axis
        eps: float, optional
            Cutoff for small elements in the resulting matrix. Defaults to 1e-10

    Returns
    -------
        NDArray
            The rotation matrix
    """

    u = u / np.linalg.norm(u)

    M = (
        np.cos(theta) * np.eye(3)
        + np.sin(theta) * crossM(u)
        + (1 - np.cos(theta)) * np.outer(u, u)
    )

    # kill off small numbers
    M[abs(M) < eps] = 0.0
    return M


def RotMa2b(a: NDArray, b: NDArray, eps: float = 1e-10) -> NDArray:
    """Definition of rotation matrix rotating unit vector a to unit vector b.

    Function returns array R such that R @ a = b holds.

    Parameters
    ----------
        a: NDArray
            First vector
        b: NDArray
            Second vector
        eps: float, optional
            Cutoff for small elements in the resulting matrix. Defaults to 1e-10

    Returns
    --------
        NDArray
            The rotation matrix with the above property
    """

    v = np.cross(a, b)
    c = a @ b
    M = np.eye(3) + crossM(v) + crossM(v) @ crossM(v) / (1 + c)

    # kill off small numbers
    M[abs(M) < eps] = 0.0
    return M


def setup_from_range(
    dh: sisl.physics.Hamiltonian,
    R: float,
    subset: Union[None, list[int], list[list[int], list[int]]] = None,
    **kwargs,
) -> tuple[sisl.physics.Hamiltonian, list[dict], list[dict]]:
    """Generates all the pairs and magnetic entities from atoms in a given radius.

    It takes all the atoms from the unit cell and generates
    all the corresponding pairs and magnetic entities in the given
    radius. It can generate pairs for a subset of of atoms,
    which can be given by the ``subset`` parameter.

    1. If subset is None all atoms can create pairs

    2. If subset is a list of integers, then all the
    possible pairs will be generated to these atoms in
    the unit cell

    3. If subset is two list, then the first list is the
    list of atoms in the unit cell (``Ri``), that can create
    pairs and the second list is the list of atoms outside
    the unit cell that can create pairs (``Rj``)

    !!!WARNING!!!
    In the third case it is really ``Ri`` and ``Rj``, that
    are given, so in some cases we could miss pairs in the
    unit cell.

    Parameters
    ----------
    dh : sisl.physics.Hamiltonian
        The sisl Hamiltonian that contains the geometry and
        atomic information
    R : float
        The radius where the pairs are found
    subset : Union[None, list[int], list[list[int], list[int]]], optional
        The subset of atoms that contribute to the pairs, by default None

    Other Parameters
    ----------------
    kwargs: otpional
        These are passed to the magnetic entity dictionary

    Returns
    -------
    magnetic_entities : list[dict]
        The magnetic entities dictionaries
    pairs : list[dict]
        The pair dictionaries
    """

    # copy so we do not overwrite
    dh = dh.copy()

    # case 1
    # if subset is not given, then use all the atoms in the
    # unit cell
    if subset is None:
        uc_atoms = range(dh.na)
        uc_out_atoms = range(dh.na)

    elif isinstance(subset, list):
        # case 2
        # if only the unit cell atoms are given
        if isinstance(subset[0], int):
            uc_atoms = subset
            uc_out_atoms = range(dh.na)

        # case 3
        # if the unit cell atoms and the atoms outside the unit cell
        # are both given
        elif isinstance(subset[0], list):
            uc_atoms = subset[0]
            uc_out_atoms = subset[1]

    pairs = []
    # the center from which we measure the distance
    for i in uc_atoms:
        center = dh.xyz[i]

        # update number of supercells based on the range from
        # the input R

        # two times the radius should be the length along each
        # lattice vector + 2 for the division
        offset = (R // np.linalg.norm(dh.cell, axis=1)) + 1
        offset *= 2
        # of offset is odd, then chose it, if even, chose the larger
        # odd number beside it
        offset += 1 - (offset % 2)
        dh.set_nsc(offset)

        # get all atoms in the range
        indices = dh.geometry.close(center, R)

        # get the supercell indices and the atom indices in
        # the shifted supercell
        aj = dh.geometry.asc2uc(indices)
        Ruc = dh.geometry.a2isc(indices)

        # this is where we fulfill the second part of condition
        # three
        mask = [k in uc_out_atoms for k in aj]
        aj = aj[mask]
        Ruc = Ruc[mask]

        ai = np.ones_like(aj) * i

        for j in range(len(ai)):
            # do not include self interaction
            if ai[j] == aj[j] and (Ruc[j] == np.array([0, 0, 0])).all():
                continue

            # append pairs
            pairs.append([ai[j], aj[j], Ruc[j][0], Ruc[j][1], Ruc[j][2]])

    # sort pairs for nicer output
    pairs = np.array(pairs)
    idx = np.lexsort((pairs[:, 4], pairs[:, 3], pairs[:, 2], pairs[:, 1], pairs[:, 0]))
    pairs = pairs[idx]

    # create magnetic entities
    atoms = np.unique(pairs[:, [0, 1]])
    magnetic_entities = [dict(atom=at, **kwargs) for at in atoms]

    # create output pair information
    out = []
    for pair in pairs:
        ai = np.where(atoms == pair[0])[0][0]
        aj = np.where(atoms == pair[1])[0][0]
        out.append(dict(ai=ai, aj=aj, Ruc=[pair[2], pair[3], pair[4]]))

    return magnetic_entities, out


def arrays_lists_equal(array1: Any, array2: Any) -> bool:
    """Compares two objects with specific rules.

    if the objects are not arrays or nested lists ending in
    arrays, then it returns False. Otherwise it goes
    down the list structure and checks all the arrays with
    np.allclose for equality. If the structure itself or any
    array is different, then it returns False. Otherwise it
    returns True. It is useful to check the Greens function
    results and the perturbations.

    Parameters
    ----------
    array1: Any
        The first object to compare
    array2: Any
        The second object to compare

    Returns
    -------
    bool:
        Wether the above described structures are equal
    """

    # if both are array, then they can be equal
    if isinstance(array1, np.ndarray) and isinstance(array2, np.ndarray):
        # the array shapes should be equal
        if array1.shape == array2.shape:
            # the array elements should be equal
            if np.allclose(array1, array2):
                return True
            else:
                return False
        else:
            return False

    # if both are lists, then they can be equal
    elif isinstance(array1, list) and isinstance(array2, list):
        # the list legngths should be equal
        if len(array1) == len(array2):
            equality = []
            # all the list elements should be equal
            for a1, a2 in zip(array1, array2):
                equality.append(arrays_lists_equal(a1, a2))
            if np.all(equality):
                return True
            else:
                return False
        else:
            return False

    # othervise they are not the desired structure
    else:
        False


def arrays_None_equal(array1: Any, array2: Any) -> bool:
    """Compares two objects with specific rules.

    if the objects are not arrays or None, then it returns
    False. Otherwise it compares the arrays.

    Parameters
    ----------
    array1: Any
        The first object to compare
    array2: Any
        The second object to compare

    Returns
    -------
    bool:
        Wether the above described structures are equal
    """

    # if both are array, then they can be equal
    if isinstance(array1, np.ndarray) and isinstance(array2, np.ndarray):
        # the array shapes should be equal
        if array1.shape == array2.shape:
            # the array elements should be equal
            if np.allclose(array1, array2):
                return True
            else:
                return False
        else:
            return False

    # if both are None, then they are equal
    elif array1 is None and array2 is None:
        return True

    # othervise they are not the desired structure
    else:
        False


def parallel_Gk(HK: NDArray, SK: NDArray, samples: NDArray, eset: int) -> NDArray:
    """Calculates the Greens function by inversion.

    It calculates the Greens function on all the energy levels at the same time.

    Parameters
    ----------
        HK: (NO, NO), NDArray
            Hamiltonian at a given k point
        SK: (NO, NO), NDArray
            Overlap Matrix at a given k point
        samples: (eset) NDArray
            Energy sample along the contour
        eset: int
            Number of energy samples along the contour

    Returns
    -------
        Gk: (eset, NO, NO), NDArray
            Green's function at a given k point
    """

    # Calculates the Greens function on all the energy levels
    return np.linalg.inv(SK * samples.reshape(eset, 1, 1) - HK)


def sequential_Gk(HK: NDArray, SK: NDArray, samples: NDArray, eset: int) -> NDArray:
    """Calculates the Greens function by inversion.

    It calculates sequentially over the energy levels.

    Parameters
    ----------
        HK: (NO, NO), NDArray
            Hamiltonian at a given k point
        SK: (NO, NO), NDArray
            Overlap Matrix at a given k point
        samples: (eset) NDArray
            Energy sample along the contour
        eset: int
            Number of energy samples along the contour

    Returns
    -------
        Gk: (eset, NO, NO), NDArray
            Green's function at a given k point
    """

    # creates an empty holder
    Gk = np.zeros(shape=(eset, HK.shape[0], HK.shape[1]), dtype="complex128")
    # fills the holder sequentially by the Greens function on a given energy
    for j in range(eset):
        Gk[j] = np.linalg.inv(SK * samples[j] - HK)

    return Gk


def onsite_projection(matrix: NDArray, idx1: NDArray, idx2: NDArray) -> NDArray:
    """It produces the slices of a matrix for the on site projection.

    The slicing is along the last two axes as these contains the orbital indexing.

    Parameters
    ----------
        matrix: (..., :, :) NDArray
            Some matrix
        idx: NDArray
            The indexes of the orbitals

    Returns
    -------
        NDArray
            Reduced matrix based on the projection
    """

    return matrix[..., idx1, :][..., idx2]


def calc_Vu(H: NDArray, Tu: NDArray) -> NDArray:
    """Calculates the local perturbation in case of a spin rotation.

    Parameters
    ----------
        H: (NO, NO) NDArray
            Hamiltonian
        Tu: (NO, NO) array_like
            Rotation around u

    Returns
    -------
        Vu1: (NO, NO) NDArray
            First order perturbed matrix
        Vu2: (NO, NO) NDArray
            Second order perturbed matrix
    """

    Vu1 = 1j / 2 * commutator(H, Tu)  # equation 100
    Vu2 = 1 / 8 * commutator(commutator(Tu, H), Tu)  # equation 100

    return Vu1, Vu2


def build_hh_ss(dh: sisl.physics.Hamiltonian) -> tuple[NDArray, NDArray]:
    """It builds the Hamiltonian and Overlap matrix from the sisl.dh class.

    It restructures the data in the SPIN BOX representation, where NS is
    the number of supercells and NO is the number of orbitals.

    Parameters
    ----------
        dh: sisl.physics.Hamiltonian
            Hamiltonian read in by sisl

    Returns
    -------
        hh: (NS, NO, NO) NDArray
            Hamiltonian in SPIN BOX representation
        ss: (NS, NO, NO) NDArray
            Overlap matrix in SPIN BOX representation
    """

    NO = dh.no  # shorthand for number of orbitals in the unit cell

    # this is known for polarized, non-collinear and spin orbit
    h11 = dh.tocsr(0)  # 0 is M11 or M11r
    # If there is spin orbit interaction in the Hamiltonian add the imaginary part, else
    # it will be zero, when we convert to complex
    if dh.spin.kind == 3:
        h11 += dh.tocsr(dh.M11i) * 1.0j
    h11 = h11.toarray().reshape(NO, dh.n_s, NO).transpose(0, 2, 1).astype("complex128")

    # this is known for polarized, non-collinear and spin orbit
    h22 = dh.tocsr(1)  # 1 is M22 or M22r
    # If there is spin orbit interaction in the Hamiltonian add the imaginary part, else
    # it will be zero, when we convert to complex
    if dh.spin.kind == 3:
        h22 += dh.tocsr(dh.M22i) * 1.0j
    h22 = h22.toarray().reshape(NO, dh.n_s, NO).transpose(0, 2, 1).astype("complex128")

    # if it is non-colinear or spin orbit, then these are known
    if dh.spin.kind == 2 or dh.spin.kind == 3:
        h12 = dh.tocsr(2)  # 2 is dh.M12r
        h12 += dh.tocsr(3) * 1.0j  # 3 is dh.M12i
        h12 = (
            h12.toarray()
            .reshape(NO, dh.n_s, NO)
            .transpose(0, 2, 1)
            .astype("complex128")
        )
    # if it is polarized then this should be zero
    elif dh.spin.kind == 1:
        h12 = np.zeros_like(h11).astype("complex128")
    else:
        raise Exception("Unpolarized DFT calculation cannot be used!")

    # if it is spin orbit, then these are known
    if dh.spin.kind == 3:
        h21 = dh.tocsr(dh.M21r)
        h21 += dh.tocsr(dh.M21i) * 1.0j
        h21 = (
            h21.toarray()
            .reshape(NO, dh.n_s, NO)
            .transpose(0, 2, 1)
            .astype("complex128")
        )
    # if it is non-colinear or polarized then this should be zero
    elif dh.spin.kind == 1 or dh.spin.kind == 2:
        h21 = np.zeros_like(h11).astype("complex128")
    else:
        raise Exception("Unpolarized DFT calculation cannot be used!")

    sov = (
        dh.tocsr(dh.S_idx)
        .toarray()
        .reshape(NO, dh.n_s, NO)
        .transpose(0, 2, 1)
        .astype("complex128")
    )

    # Reorganization of Hamiltonian and overlap matrix elements to SPIN BOX representation
    U = np.vstack(
        [
            np.kron(np.eye(NO, dtype=int), np.array([1, 0])),
            np.kron(np.eye(NO, dtype=int), np.array([0, 1])),
        ]
    )

    # This is the permutation that transforms ud1ud2 to u12d12
    # That is this transforms FROM SPIN BOX to ORBITAL BOX => U
    # the inverse transformation is U.T u12d12 to ud1ud2
    # That is FROM ORBITAL BOX to SPIN BOX => U.T

    # progress bar
    bar = _tqdm(None, total=3 * dh.n_s, desc="Setting up Hamiltonian")

    # From now on everything is in SPIN BOX!!
    if CONFIG.is_CPU:
        hh = []
        for i in range(dh.n_s):
            row1 = np.hstack([h11[:, :, i], h12[:, :, i]])
            row2 = np.hstack([h21[:, :, i], h22[:, :, i]])
            block = np.vstack([row1, row2])
            hh.append(U.T @ block @ U)
            bar.update()
        hh = np.array(hh)

        ss = []
        for i in range(dh.n_s):
            row1 = np.hstack([sov[:, :, i], sov[:, :, i] * 0])
            row2 = np.hstack([sov[:, :, i] * 0, sov[:, :, i]])
            block = np.vstack([row1, row2])
            ss.append(U.T @ block @ U)
            bar.update()
        ss = np.array(ss)

        for i in range(dh.n_s):
            j = dh.lattice.sc_index(-dh.sc_off[i])
            h1, h1d = hh[i], hh[j]
            hh[i], hh[j] = (h1 + h1d.T.conj()) / 2, (h1d + h1.T.conj()) / 2
            s1, s1d = ss[i], ss[j]
            ss[i], ss[j] = (s1 + s1d.T.conj()) / 2, (s1d + s1.T.conj()) / 2
            bar.update()

    elif CONFIG.is_GPU:
        h11 = cp.array(h11)
        h12 = cp.array(h12)
        h21 = cp.array(h21)
        h22 = cp.array(h22)
        sov = cp.array(sov)
        U = cp.array(U)

        hh = []
        for i in range(dh.n_s):
            row1 = cp.hstack([h11[:, :, i], h12[:, :, i]])
            row2 = cp.hstack([h21[:, :, i], h22[:, :, i]])
            block = cp.vstack([row1, row2])
            hh.append(U.T @ block @ U)
            bar.update()

        ss = []
        for i in range(dh.n_s):
            row1 = cp.hstack([sov[:, :, i], sov[:, :, i] * 0])
            row2 = cp.hstack([sov[:, :, i] * 0, sov[:, :, i]])
            block = cp.vstack([row1, row2])
            ss.append(U.T @ block @ U)
            bar.update()

        for i in range(dh.n_s):
            j = dh.lattice.sc_index(-dh.sc_off[i])
            h1, h1d = hh[i], hh[j]
            hh[i], hh[j] = (h1 + h1d.T.conj()) / 2, (h1d + h1.T.conj()) / 2
            s1, s1d = ss[i], ss[j]
            ss[i], ss[j] = (s1 + s1d.T.conj()) / 2, (s1d + s1.T.conj()) / 2
            bar.update()

        hh = np.array([h.get() for h in hh])
        ss = np.array([s.get() for s in ss])

    else:
        raise ValueError(f"Unknown architecture: {CONFIG.architecture}")

    return hh, ss


def make_contour(
    emin: float = -20, emax: float = 0.0, enum: int = 42, p: float = 150
) -> tuple[NDArray, NDArray]:
    """A more sophisticated contour generator.

    Calculates the parameters for the complex contour integral. It uses the
    Legendre-Gauss quadrature method. It returns a class that contains
    the information for the contour integral.

    Parameters
    ----------
        emin: int, optional
            Energy minimum of the contour. Defaults to -20
        emax: float, optional
            Energy maximum of the contour. Defaults to 0.0, so the Fermi level
        enum: int, optional
            Number of sample points along the contour. Defaults to 42
        p: int, optional
            Shape parameter that describes the distribution of the sample points. Defaults to 150

    Returns
    -------
        ze: NDArray
            Contour points
        we: NDArray
            Weights along the contour
    """

    x, wl = roots_legendre(enum)
    R = (emax - emin) / 2  # radius
    z0 = (emax + emin) / 2  # center point
    y1 = -np.log(1 + np.pi * p)  # lower bound
    y2 = 0  # upper bound

    y = (y2 - y1) / 2 * x + (y2 + y1) / 2
    phi = (np.exp(-y) - 1) / p  # angle parameter
    ze = z0 + R * np.exp(1j * phi)  # complex points for path
    we = -(y2 - y1) / 2 * np.exp(-y) / p * 1j * (ze - z0) * wl

    return ze, we


def make_kset(kset: Union[list, NDArray] = np.array([1, 1, 1])) -> NDArray:
    """Simple k-grid generator to sample the Brillouin zone.

    Parameters
    ----------
        kset: Union[list, NDArray]
            The number of k points in each direction

    Returns
    -------
        NDArray
            An array of k points that uniformly sample the Brillouin zone in the given directions
    """

    kset = np.array(kset)
    mpi = np.floor(-kset / 2) + 1
    x = np.arange(mpi[0], np.floor(kset[0] / 2 + 1), 1) / kset[0]
    y = np.arange(mpi[1], np.floor(kset[1] / 2 + 1), 1) / kset[1]
    z = np.arange(mpi[2], np.floor(kset[2] / 2 + 1), 1) / kset[2]

    x, y, z = np.meshgrid(x, y, z)
    kset = np.array([x.flatten(), y.flatten(), z.flatten()]).T

    return kset


def hsk(
    H: NDArray, S: NDArray, sc_off: list, k: tuple = (0, 0, 0)
) -> tuple[NDArray, NDArray]:
    """Speed up Hk and Sk generation.

    Calculates the Hamiltonian and the Overlap matrix at a given k point. It is faster that the sisl version.

    Parameters
    ----------
        H: NDArray
            Hamiltonian in spin box form
        ss: NDArray
            Overlap matrix in spin box form
        sc_off: list
            supercell indexes of the Hamiltonian
        k: tuple, optional
            The k point where the matrices are set up. Defaults to (0, 0, 0)

    Returns
    -------
        NDArray
            Hamiltonian at the given k point
        NDArray
            Overlap matrix at the given k point
    """

    # this two conversion lines are from the sisl source
    k = np.asarray(k, np.float64)
    k.shape = (-1,)

    # this generates the list of phases
    phases = np.exp(-1j * 2 * np.pi * k @ sc_off.T)

    # phases applied to the hamiltonian
    HK = np.einsum("abc,a->bc", H, phases)
    SK = np.einsum("abc,a->bc", S, phases)

    return HK, SK


if __name__ == "__main__":
    pass
