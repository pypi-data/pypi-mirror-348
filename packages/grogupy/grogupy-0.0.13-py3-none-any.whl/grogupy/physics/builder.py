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
import copy
import io
import os
import warnings
from typing import Union

import numpy as np
import sisl
from numpy.typing import NDArray

from .. import __version__
from .._core.utilities import RotMa2b, setup_from_range
from .._tqdm import _tqdm
from ..batch.timing import DefaultTimer
from ..config import CONFIG
from .contour import Contour
from .hamiltonian import Hamiltonian
from .kspace import Kspace
from .magnetic_entity import MagneticEntity
from .pair import Pair

try:
    import pytest

    @pytest.fixture()
    def setup():
        k, c = Kspace(), Contour(100, 100, -20)
        h = Hamiltonian(
            "/Users/danielpozsar/Downloads/Fe3GeTe2/Fe3GeTe2.fdf",
            [0, 0, 1],
        )
        return k, c, h

except:
    pass


class Builder:
    """This class contains the data and the methods related to the Simulation.

    Parameters
    ----------
    ref_xcf_orientations: Union[list, NDArray], optional
        The reference directions. The perpendicular directions are created by rotating
        the x,y,z frame to the given reference directions, by default [[1,0,0], [0,1,0], [0,0,1]]
    matlabmode: bool, optional
        Wether to use the convention of the Matlab implementation, by default False

    Examples
    --------
    Creating a Simulation from the DFT exchange field orientation,  Hamiltonian, Kspace
    and Contour.

    >>> kspace, contour, hamiltonian = getfixture('setup')
    >>> simulation = Builder(np.array([[1,0,0], [0,1,0], [0,0,1]]))
    >>> simulation.add_kspace(kspace)
    >>> simulation.add_contour(contour)
    >>> simulation.add_hamiltonian(hamiltonian)
    >>> simulation
    <grogupy.Builder npairs=0, numk=1, kset=[1 1 1], eset=100>

    Methods
    -------
    add_kspace(kspace) :
        Adds the k-space information to the instance.
    add_contour(contour) :
        Adds the energy contour information to the instance.
    add_hamiltonian(hamiltonian) :
        Adds the Hamiltonian and geometrical information to the instance.
    add_magnetic_entities(magnetic_entities) :
        Adds a MagneticEntity or a list of MagneticEntity to the instance.
    add_pairs(pairs) :
        Adds a Pair or a list of Pair to the instance.
    create_magnetic_entities(magnetic_entities) :
        Creates a list of MagneticEntity from a list of dictionaries.
    create_pairs(pairs) :
        Creates a list of Pair from a list of dictionaries.
    solve() :
        Wrapper for Greens function solver.
    to_magnopy(): str
        The magnopy output file as a string
    save_magnopy(outfile) :
        Creates a magnopy input file based on a path.
    save_pickle(outfile) :
        It dumps the simulation parameters to a pickle file.
    copy() :
        Return a copy of this Pair

    Attributes
    ----------
    kspace: Union[None, Kspace]
        The k-space part of the integral
    contour: Union[None, Contour]
        The energy part of the integral
    hamiltonian: Union[None, Hamiltonian]
        The Hamiltonian of the previous article
    magnetic_entities: list[MagneticEntity]
        List of magnetic entities
    pairs: list[Pair]
        List of pairs
    greens_function_solver: {"Sequential", "Parallel"}
        The solution method for the Hamiltonian inversion, by default "Sequential"
    exchange_solver: {"Fit", "grogupy"}
        The solution method for the exchange tensor, by default "Fit"
    anisotropy_solver: {"Fit", "grogupy"}
        The solution method for the anisotropy tensor, by default "grogupy"
    ref_xcf_orientations: NDArray
        The reference directions and two perpendicular direction. Every element is a
        dictionary, wth two elements, 'o', the reference direction and 'vw', the two
        perpendicular directions and a third direction that is the linear combination of
        the two
    architecture: {"CPU", "GPU"}, optional
        The architecture of the machine that grogupy is run on, by default 'CPU'
    SLURM_ID: str
        The ID of the SLURM job, if available, else 'Could not be determined.'
    _dh: sisl.physics.Hamiltonian
        The sisl Hamiltonian from the instance Hamiltonian
    scf_xcf_orientation: NDArray
        The DFT exchange filed orientation from the instance Hamiltonian
    infile: str
        Input path to the .fdf file
    times: grogupy.batch.timing.DefaultTimer
        It contains and measures runtime
    """

    root_node = 0

    def __init__(
        self,
        ref_xcf_orientations: Union[list, NDArray] = [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
        matlabmode: bool = False,
    ) -> None:
        """Initialize simulation."""

        #: Contains a DefaultTimer instance to measure runtime
        self.times: DefaultTimer = DefaultTimer()
        #: Contains a Kspace instance
        self.kspace: Union[None, Kspace] = None
        #: Contains a Contour instance
        self.contour: Union[None, Contour] = None
        #: Contains a Hamiltonian instance
        self.hamiltonian: Union[None, Hamiltonian] = None

        #: The list of magnetic entities
        self.magnetic_entities: list[MagneticEntity] = []
        #: The list of pairs
        self.pairs: list[Pair] = []

        # fix the architecture
        self.__low_memory_mode = True
        self.__greens_function_solver: str = "Sequential"
        self.__max_g_per_loop: int = 10000
        self.__parallel_mode: str = "K"
        self.__architecture = CONFIG.architecture

        # fix the matlab compatibility
        self.__matlabmode = matlabmode
        if self.__matlabmode:
            self.__exchange_solver: str = "grogupy"
            self.__anisotropy_solver: str = "grogupy"
        else:
            self.__exchange_solver: str = "Fit"
            self.__anisotropy_solver: str = "Fit"

        # this is the original three axes o is z and vw is x and y
        x = np.array([1, 0, 0], dtype=float)
        y = np.array([0, 1, 0], dtype=float)
        z = np.array([0, 0, 1], dtype=float)
        # for every given orientation we rotate the x,y,z coordinate system
        orientations = []
        for a in np.array(ref_xcf_orientations):
            # normalize, just in case
            a = a / np.linalg.norm(a)
            ztoa = RotMa2b(z, a)
            o = ztoa @ z
            v = ztoa @ x
            w = ztoa @ y
            if self.__anisotropy_solver.lower()[0] == "g":
                # add third orientation required for off-diagonal
                # anisotropy elements
                vw_mix = (v + w) / np.linalg.norm(v + w)
                orientations.append(dict(o=o, vw=[v, w, vw_mix]))
            else:
                orientations.append(dict(o=o, vw=[v, w]))

        self.ref_xcf_orientations: list[dict] = orientations
        if self.__matlabmode:
            self.ref_xcf_orientations = [
                dict(
                    #                    o=np.array([1, 0, 0]), vw=[np.array([0, 0, -1]), np.array([0, 1, 0])]
                    o=np.array([1, 0, 0]),
                    vw=[np.array([0, 1, 0]), np.array([0, 0, 1])],
                ),
                dict(
                    #                    o=np.array([0, 1, 0]), vw=[np.array([1, 0, 0]), np.array([0, 0, -1])]
                    o=np.array([0, 1, 0]),
                    vw=[np.array([1, 0, 0]), np.array([0, 0, 1])],
                ),
                dict(
                    #                    o=np.array([0, 0, 1]), vw=[np.array([1, 0, 0]), np.array([0, 1, 0])]
                    o=np.array([0, 0, 1]),
                    vw=[np.array([1, 0, 0]), np.array([0, 1, 0])],
                ),
            ]
            for ref in self.ref_xcf_orientations:
                v = ref["vw"][0]
                w = ref["vw"][1]
                vw = (v + w) / np.sqrt(2)
                ref["vw"].append(vw)
            warnings.warn(
                "Matlabmode is used, the exchange field reference directions were set to x,y,z!"
            )

        self._rotated_hamiltonians: list[Hamiltonian] = []

        try:
            self.SLURM_ID: str = os.environ["SLURM_JOB_ID"]
        except:
            self.SLURM_ID: str = "Could not be determined."

        self.__version = __version__

        self.times.measure("setup", restart=True)

    def __getstate__(self):
        state = self.__dict__.copy()
        state["times"] = state["times"].__getstate__()
        state["contour"] = state["contour"].__getstate__()
        state["kspace"] = state["kspace"].__getstate__()
        state["hamiltonian"] = state["hamiltonian"].__getstate__()

        out = []
        for h in state["_rotated_hamiltonians"]:
            out.append(h.__getstate__())
        state["_rotated_hamiltonians"] = out

        out = []
        for m in state["magnetic_entities"]:
            out.append(m.__getstate__())
        state["magnetic_entities"] = out

        out = []
        for p in state["pairs"]:
            out.append(p.__getstate__())
        state["pairs"] = out

        return state

    def __setstate__(self, state):
        times = object.__new__(DefaultTimer)
        times.__setstate__(state["times"])
        state["times"] = times

        contour = object.__new__(Contour)
        contour.__setstate__(state["contour"])
        state["contour"] = contour

        kspace = object.__new__(Kspace)
        kspace.__setstate__(state["kspace"])
        state["kspace"] = kspace

        hamiltonian = object.__new__(Hamiltonian)
        hamiltonian.__setstate__(state["hamiltonian"])
        state["hamiltonian"] = hamiltonian

        out = []
        for h in state["_rotated_hamiltonians"]:
            temp = object.__new__(Hamiltonian)
            temp.__setstate__(h)
            out.append(temp)
        state["_rotated_hamiltonians"] = out

        out = []
        for m in state["magnetic_entities"]:
            temp = object.__new__(MagneticEntity)
            temp.__setstate__(m)
            out.append(temp)
        state["magnetic_entities"] = out

        out = []
        for p in state["pairs"]:
            temp = object.__new__(Pair)
            temp.__setstate__(p)
            out.append(temp)
        state["pairs"] = out

        self.__dict__ = state

    def __eq__(self, value):
        if isinstance(value, Builder):
            if (
                self.times == value.times
                and self.kspace == value.kspace
                and self.contour == value.contour
                and self.hamiltonian == value.hamiltonian
                and self.__low_memory_mode == value.__low_memory_mode
                and self.__greens_function_solver == value.__greens_function_solver
                and self.__max_g_per_loop == value.__max_g_per_loop
                and self.__parallel_mode == value.__parallel_mode
                and self.__architecture == value.__architecture
                and self.__matlabmode == value.__matlabmode
                and self.__exchange_solver == value.__exchange_solver
                and self.__anisotropy_solver == value.__anisotropy_solver
                and self.SLURM_ID == value.SLURM_ID
                and self.__version == value.__version
            ):
                if len(self._rotated_hamiltonians) != len(value._rotated_hamiltonians):
                    return False
                if len(self.magnetic_entities) != len(value.magnetic_entities):
                    return False
                if len(self.pairs) != len(value.pairs):
                    return False
                if len(self.ref_xcf_orientations) != len(value.ref_xcf_orientations):
                    return False

                for i in range(len(self.ref_xcf_orientations)):
                    for k in self.ref_xcf_orientations[i].keys():
                        if not np.allclose(
                            self.ref_xcf_orientations[i][k],
                            value.ref_xcf_orientations[i][k],
                        ):
                            return False

                for one, two in zip(
                    self._rotated_hamiltonians, value._rotated_hamiltonians
                ):
                    if one != two:
                        return False

                for one, two in zip(self.magnetic_entities, value.magnetic_entities):
                    if one != two:
                        return False

                for one, two in zip(self.pairs, value.pairs):
                    if one != two:
                        return False
                return True
            return False
        return False

    def __str__(self) -> str:
        """It prints the parameters and the description of the job.

        Args:
            self :
                It contains the simulations parameters
        """

        section = "================================================================================"
        newline = "\n"

        out = ""
        out += section + newline
        out += f"grogupy version: {self.__version}" + newline
        out += f"Input file: {self.infile}" + newline
        out += f"Spin mode: {self.hamiltonian._spin_state}" + newline
        out += f"Number of orbitals: {self.hamiltonian.NO}" + newline
        out += section + newline
        out += f"SLURM job ID: {self.SLURM_ID}" + newline
        out += f"Architecture: {self.__architecture}" + newline
        if self.__architecture == "CPU":
            out += (
                f"Number of nodes in the parallel cluster: {CONFIG.parallel_size}"
                + newline
            )
        elif self.__architecture == "GPU":
            out += f"Number of GPUs in the cluster: {CONFIG.parallel_size}" + newline
        out += f"Parallelization is over: {self.parallel_mode}" + newline
        out += (
            f"Solver used for Greens function calculation: {self.greens_function_solver}"
            + newline
        )
        if self.greens_function_solver[0].lower() == "s":
            max_g = self.__max_g_per_loop
        else:
            max_g = self.contour.eset
        out += f"Maximum number of Greens function samples per batch: {max_g}" + newline

        out += f"Solver used for Exchange tensor: {self.exchange_solver}" + newline
        out += f"Solver used for Anisotropy tensor: {self.anisotropy_solver}" + newline
        out += section + newline

        out += f"Cell [Ang]:" + newline

        bio = io.BytesIO()
        np.savetxt(bio, self.hamiltonian.cell)
        cell = bio.getvalue().decode("latin1")
        out += cell

        out += section + newline
        out += f"DFT axis: {self.scf_xcf_orientation}" + newline
        out += "Quantization axis and perpendicular rotation directions:" + newline
        for ref in self.ref_xcf_orientations:
            out += f"{ref['o']} --> {ref['vw']}" + newline

        out += section + newline
        out += "Parameters for the Brillouin zone sampling:" + newline
        out += f"Number of k points: {self.kspace.kset.prod()}" + newline
        out += f"K points in each directions: {self.kspace.kset}" + newline
        out += "Parameters for the contour integral:" + newline
        out += f"Eset: {self.contour.eset}" + newline
        out += f"Esetp: {self.contour.esetp}" + newline
        if self.contour.automatic_emin:
            out += (
                f"Ebot: {self.contour.emin}        WARNING: This was automatically determined!"
                + newline
            )
        else:
            out += f"Ebot: {self.contour.emin}" + newline
        out += f"Etop: {self.contour.emax}" + newline
        out += section + newline

        return out

    def __repr__(self) -> str:
        if self.kspace is None:
            NK = "None"
            kset = "None"
        else:
            NK = self.kspace.NK
            kset = self.kspace.kset
        if self.contour is None:
            eset = "None"
        else:
            eset = self.contour.eset

        string = f"<grogupy.Builder npairs={len(self.pairs)}, numk={NK}, kset={kset}, eset={eset}>"

        return string

    @property
    def NO(self) -> int:
        """The number of orbitals in the Hamiltonian."""

        if self.hamiltonian is None:
            raise Exception("You have to add Hamiltonian first!")

        return self.hamiltonian.NO

    @property
    def matlabmode(self) -> bool:
        """Wether to force compatibility with matlab or not."""
        return self.__matlabmode

    @property
    def exchange_solver(self) -> str:
        """The solver used for the exchange tensor calculation."""
        return self.__exchange_solver

    @exchange_solver.setter
    def exchange_solver(self, value: str) -> None:
        if value.lower()[0] == "f":  # fit
            if self.__matlabmode:
                raise Exception(
                    f"Matlab does not support this solution method: {value}"
                )
            else:
                self.__exchange_solver: str = "Fit"
        elif value.lower()[0] == "g":  # grogupy
            self.__exchange_solver: str = "grogupy"
        else:
            raise Exception(f"Unrecognized solution method: {value}")

    @property
    def anisotropy_solver(self) -> str:
        """The solver used for the anisotropy tensor calculation."""
        return self.__anisotropy_solver

    @anisotropy_solver.setter
    def anisotropy_solver(self, value: str) -> None:
        if value.lower()[0] == "f":  # fit
            if self.__matlabmode:
                raise Exception(
                    f"Matlab does not support this solution method: {value}"
                )
            else:
                self.__anisotropy_solver: str = "Fit"
                # add the linear combination of the orientations
                for ref_xcf in self.ref_xcf_orientations:
                    if len(ref_xcf["vw"]) == 3:
                        ref_xcf["vw"].pop()

        elif value.lower()[0] == "g":  # grogupy
            self.__anisotropy_solver: str = "grogupy"
            # add the linear combination of the orientations
            for ref_xcf in self.ref_xcf_orientations:
                if len(ref_xcf["vw"]) == 2:
                    vw_mix = (ref_xcf["vw"][0] + ref_xcf["vw"][1]) / np.linalg.norm(
                        ref_xcf["vw"][0] + ref_xcf["vw"][1]
                    )
                    ref_xcf["vw"].append(vw_mix)
        else:
            raise Exception(f"Unrecognized solution method: {value}")

    @property
    def low_memory_mode(self) -> str:
        """The memory mode of the calculation."""
        return self.__low_memory_mode

    @low_memory_mode.setter
    def low_memory_mode(self, value: bool) -> None:
        if value == False:
            self.__low_memory_mode = False
        elif value == True:
            self.__low_memory_mode = True
        else:
            raise Exception("This must be Bool!")

    @property
    def greens_function_solver(self) -> str:
        """The solution method for the Hamiltonian inversion, by default "Sequential"."""
        return self.__greens_function_solver

    @greens_function_solver.setter
    def greens_function_solver(self, value: str) -> None:
        if value.lower()[0] == "s":
            self.__greens_function_solver = "Sequential"
        elif value.lower()[0] == "p":
            self.__greens_function_solver = "Parallel"
        else:
            raise Exception(
                f"{value} is not a permitted Green's function solver, when the architecture is {self.__architecture}."
            )

    @property
    def max_g_per_loop(self) -> int:
        """Maximum number of greens function samples per loop."""
        return self.__max_g_per_loop

    @max_g_per_loop.setter
    def max_g_per_loop(self, value) -> None:
        if (value - int(value)) < 1e-5 and value >= 0:
            value = int(value)
            self.__max_g_per_loop = value
        else:
            raise Exception("It should be a positive integer.")

    @property
    def parallel_mode(self) -> str:
        """The parallelization mode for the Hamiltonian inversions, by default "K"."""
        return self.__parallel_mode

    @property
    def architecture(self) -> str:
        """The architecture of the machine that grogupy is run on, by default 'CPU'."""
        return self.__architecture

    @property
    def _dh(self) -> sisl.physics.Hamiltonian:
        """``sisl`` Hamiltonian object used in the input."""
        return self.hamiltonian._dh

    @property
    def _ds(self) -> sisl.physics.DensityMatrix:
        """``sisl`` density matrix object used in the input."""
        return self.hamiltonian._ds

    @property
    def geometry(self) -> sisl.geometry:
        """``sisl`` geometry object."""
        return self.hamiltonian._dh.geometry

    @property
    def scf_xcf_orientation(self) -> NDArray:
        """Exchange field orientation in the DFT calculation."""
        return self.hamiltonian.scf_xcf_orientation

    @property
    def infile(self) -> str:
        """Input file used to build the Hamiltonian."""
        return self.hamiltonian.infile

    @property
    def version(self) -> str:
        """Version of grogupy."""
        return self.__version

    def to_magnopy(
        self,
        magnetic_moment: str = "total",
        precision: Union[None, int] = None,
        comments: bool = True,
    ) -> str:
        """Returns the magnopy input file as string.

        It is useful for dumping information to the standard output on
        runtime.

        Parameters
        ----------
        magnetic_moment: str, optional
            It switches the used spin moment in the output, can be 'total'
            for the whole atom or atoms involved in the magnetic entity or
            'local' if we only use the part of the mulliken projections that
            are exactly on the magnetic entity, which may be just a subshell
            of the atom, by default 'total'
        precision: Union[None, int], optional
            The precision of the magnetic parameters in the output, if None
            everything is written, by default None
        comments: bool, optional
            Wether to add comments in the beginning of file, by default True

        Returns
        -------
        str
            Magnopy input file
        """

        if precision is not None:
            if not isinstance(precision, int):
                warnings.warn(
                    f"precision must by an integer, but it is {type(precision)}. It was set to None."
                )
                precision = None
        if precision is None:
            precision = 30

        section = "================================================================================"
        subsection = "--------------------------------------------------------------------------------"
        newline = "\n"

        out = ""
        if comments:
            out += "\n".join(["# " + row for row in self.__str__().split("\n")])
            out += newline
        out += section + newline
        out += f"cell Angstrom" + newline

        bio = io.BytesIO()
        np.savetxt(bio, self.hamiltonian.cell)
        cell = bio.getvalue().decode("latin1")
        out += cell

        out += section + newline
        out += "atoms Angstrom" + newline
        out += "name\tx\ty\tz\tSx\tSy\tSz\t# Q"
        out += newline
        for mag_ent in self.magnetic_entities:
            out += mag_ent.tag + " "
            out += f"{mag_ent._xyz.mean(axis=0)[0]} {mag_ent._xyz.mean(axis=0)[1]} {mag_ent._xyz.mean(axis=0)[2]} "
            if magnetic_moment[0].lower() == "l":
                out += f"{mag_ent.local_Sx} {mag_ent.local_Sy} {mag_ent.local_Sz} # {mag_ent.local_Q}"
            else:
                out += f"{mag_ent.total_Sx} {mag_ent.total_Sy} {mag_ent.total_Sz} # {mag_ent.total_Q}"
            out += newline
        out += section + newline
        out += "notation" + newline
        out += "double-counting True" + newline
        out += "spin-normalized True" + newline
        out += f"exchange-factor {0.5}" + newline
        out += f"on-site-factor {1}" + newline

        out += section + newline
        out += "exchange meV" + newline
        for pair in self.pairs:
            out += subsection + newline
            tag = pair.tags[0] + " " + pair.tags[1]
            out += tag + " " + " ".join(map(str, pair.supercell_shift))
            out += f" # distance [Ang]: {pair.distance}" + newline
            out += "isotropic " + str(np.round(pair.J_iso_meV, precision)) + newline
            D = np.around(pair.D_meV, decimals=precision)
            out += "DMI " + f"{D[0]} {D[1]} {D[2]}" + " # Dx Dy Dz" + newline
            J = np.around(pair.J_meV - np.eye(3) * pair.J_iso_meV, decimals=precision)
            out += (
                "symmetric-anisotropy "
                + f"{J[0,0]} {J[1,1]} {J[0,1]} {J[0,2]} {J[1,2]}"
                + " # Sxx Syy Sxy Sxz Syz"
                + newline
            )
        out += subsection + newline + section + newline

        out += "on-site meV" + newline
        for mag_ent in self.magnetic_entities:
            out += subsection + newline
            out += mag_ent.tag + newline
            K = np.around(mag_ent.K_meV, decimals=precision)
            out += f"{K[0,0]} {K[1,1]} {K[2,2]} {K[0,1]} {K[0,2]} {K[1,2]}"
            out += " # Kxx Kyy Kzz Kxy Kxz Kyz" + newline

        out += subsection + newline + section + newline

        return out

    def add_kspace(self, kspace: Kspace) -> None:
        """Adds the k-space information to the instance.

        Parameters
        ----------
        kspace: Kspace
            This class contains the information of the k-space
        """

        if isinstance(kspace, Kspace):
            self.kspace = kspace
        else:
            raise Exception(f"Bad type for Kspace: {type(kspace)}")

    def add_contour(self, contour: Contour) -> None:
        """Adds the energy contour information to the instance.

        Parameters
        ----------
        contour: Contour
            This class contains the information of the energy contour
        """

        if isinstance(contour, Contour):
            self.contour = contour
        else:
            raise Exception(f"Bad type for Contour: {type(contour)}")

    def add_hamiltonian(self, hamiltonian: Hamiltonian) -> None:
        """Adds the Hamiltonian and geometrical information to the instance.

        Parameters
        ----------
        hamiltonian: Hamiltonian
            This class contains the information of the Hamiltonian
        """

        if isinstance(hamiltonian, Hamiltonian):
            self.hamiltonian = hamiltonian
        else:
            raise Exception(f"Bad type for Hamiltonian: {type(hamiltonian)}")

    def setup_from_range(
        self,
        R: float,
        subset: Union[None, list[int], list[list[int], list[int]]] = None,
        **kwargs,
    ) -> None:
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
        R : float
            The radius where the pairs are found
        subset : Union[None, list[int], list[list[int], list[int]]]
            The subset of atoms that contribute to the pairs, by
            default None

        Other Parameters
        ----------------
        **kwargs: otpional
            These are passed to the magnetic entity dictionary

        """

        magnetic_entities, pairs = setup_from_range(self._dh, R, subset, **kwargs)

        self.add_magnetic_entities(magnetic_entities)
        self.add_pairs(pairs)

    def create_magnetic_entities(
        self, magnetic_entities: Union[dict, list[dict]]
    ) -> list[MagneticEntity]:
        """Creates a list of MagneticEntity from a list of dictionaries.

        The dictionaries must contain an acceptable combination of `atom`, `l` and
        `orb`, based on the accepted input for MagneticEntity. The Hamiltonian is
        taken from the instance Hamiltonian.

        Parameters
        ----------
        magnetic_entities: Union[dict, list[dict]]
            The list of dictionaries or a single dictionary

        Returns
        -------
        list[MagneticEntity]
            List of MagneticEntity instances

        Raise
        -----
        Exception
            Hamiltonian is not added to the instance
        """

        if self.hamiltonian is None:
            raise Exception("First you need to add the Hamiltonian!")

        if isinstance(magnetic_entities, dict):
            magnetic_entities = [magnetic_entities]

        out = []
        for mag_ent in magnetic_entities:
            out.append(MagneticEntity((self._dh, self._ds), **mag_ent))

        return out

    def create_pairs(self, pairs: Union[dict, list[dict]]) -> list[Pair]:
        """Creates a list of Pair from a list of dictionaries.

        The dictionaries must contain `ai`, `aj` and `Ruc`, based on the accepted
        input from Pair. If `Ruc` is not given, then it is (0,0,0), by default.
        The Hamiltonian is taken from the instance Hamiltonian.

        Parameters
        ----------
        pairs: Union[dict, list[dict]]
            The list of dictionaries or a single dictionary

        Returns
        -------
        list[Pair]
            List of Pair instances

                    Raise
        -----
        Exception
            Hamiltonian is not added to the instance
        Exception
            Magnetic entities are not added to the instance
        """

        if self.hamiltonian is None:
            raise Exception("First you need to add the Hamiltonian!")

        if len(self.magnetic_entities) == 0:
            raise Exception("First you need to add the magnetic entities!")

        if isinstance(pairs, dict):
            pairs = [pairs]

        out = []
        for pair in pairs:
            ruc = pair.get("Ruc", np.array([0, 0, 0]))
            m1 = self.magnetic_entities[pair["ai"]]
            m2 = self.magnetic_entities[pair["aj"]]
            out.append(Pair(m1, m2, ruc))

        return out

    def add_magnetic_entities(
        self,
        magnetic_entities: Union[
            dict, MagneticEntity, list[Union[dict, MagneticEntity]]
        ],
    ) -> None:
        """Adds a MagneticEntity or a list of MagneticEntity to the instance.

        It dumps the data to the `magnetic_entities` instance parameter. If a list
        of dictionaries are given, first it tries to convert them to magnetic entities.

        Parameters
        ----------
        magnetic_entities : Union[dict, MagneticEntity, list[Union[dict, MagneticEntity]]]
            Data to add to the instance
        """

        # if it is not a list, then convert
        if not isinstance(magnetic_entities, list):
            magnetic_entities = [magnetic_entities]

        # iterate over magnetic entities
        for mag_ent in _tqdm(magnetic_entities, desc="Add magnetic entities"):
            # if it is a MagneticEntity there is nothing to do
            if isinstance(mag_ent, MagneticEntity):
                pass

            # if it is a dictionary
            elif isinstance(mag_ent, dict):
                mag_ent = self.create_magnetic_entities(mag_ent)[0]

            else:
                raise Exception(f"Bad type for MagneticEntity: {type(mag_ent)}")

            # add magnetic entities
            self.magnetic_entities.append(mag_ent)

    def add_pairs(self, pairs: Union[dict, Pair, list[Union[dict, Pair]]]) -> None:
        """Adds a Pair or a list of Pair to the instance.

        It dumps the data to the ``pairs`` instance parameter. If a list
        of dictionaries are given, first it tries to convert them to pairs.

        Parameters
        ----------
        pairs : Union[dict, Pair, list[Union[dict, Pair]]]
            Data to add to the instance
        """

        # if it is not a list, then convert
        if not isinstance(pairs, list):
            pairs = [pairs]

        # iterate over pairs
        for pair in _tqdm(pairs, desc="Add pairs"):
            # if it is a Pair there is nothing to do
            if isinstance(pair, Pair):
                pass

            # if it is a dictionary
            elif isinstance(pair, dict):
                pair = self.create_pairs(pair)[0]

            else:
                raise Exception(f"Bad type for Pair: {type(pair)}")

            # add pairs
            self.pairs.append(pair)

    def solve(self, print_memory: bool = False) -> None:
        """Wrapper for Greens function solver.

        It uses the parallelization over k-points, energy and directions if ``solver``
        is `all` and it uses the parallel over k solver if ``solver`` is `k`.

        Parameters
        ----------
        print_memory: bool, optional
            It can be turned on to print extra memory info, by default False
        """

        # reset times
        self.times.restart()

        # check to optimize calculation
        if (
            self.anisotropy_solver.lower()[0] == "g"
            or self.exchange_solver.lower()[0] == "g"
        ) and len(self.ref_xcf_orientations) > 3:
            warnings.warn(
                "There are unnecessary orientations for the anisotropy or the exchange solver!"
            )

        elif (
            self.anisotropy_solver.lower()[0] == "f"
            or self.exchange_solver.lower()[0] == "f"
        ) and np.array([len(i["vw"]) > 2 for i in self.ref_xcf_orientations]).any():
            warnings.warn(
                "There are unnecessary perpendicular directions for the anisotropy or exchange solver!"
            )

        # choose architecture solver
        if self.__architecture.lower()[0] == "c":  # cpu
            from .._core.cpu_solvers import solve_parallel_over_k
        elif self.__architecture.lower()[0] == "g":  # gpu
            from .._core.gpu_solvers import solve_parallel_over_k
        else:
            raise Exception(f"Unknown architecture: {self.__architecture}")

        solve_parallel_over_k(self, print_memory)

        self.times.measure("solution", restart=True)

    def copy(self):
        """Returns the deepcopy of the instance.

        Returns
        -------
        Hamiltonian
            The copied instance.
        """

        return copy.deepcopy(self)

    def a2M(
        self, atom: Union[int, list[int]], mode: str = "partial"
    ) -> list[MagneticEntity]:
        """Returns the magnetic entities that contains the given atoms.

        The atoms are indexed from the sisl Hamiltonian.

        Parameters
        ----------
        atom : Union[int, list[int]]
            Atomic indices from the sisl Hamiltonian
        mode : {"partial", "complete"}, optional
            Wether to completely or partially match the atoms to the
            magnetic entities, by default "partial"
        Returns
        -------
        list[MagneticEntity]
            List of MagneticEntities that contain the given atoms
        """

        if isinstance(atom, int):
            atom = [atom]

        # partial matching
        if mode.lower()[0] == "p":
            M: list = []
            for at in atom:
                for mag_ent in self.magnetic_entities:
                    if at in mag_ent.atom:
                        M.append(mag_ent)

        # complete matching
        elif mode.lower()[0] == "c":
            for at in atom:
                for mag_ent in self.magnetic_entities:
                    if at == mag_ent.atom:
                        return [mag_ent]

        else:
            raise Exception(f"Unknown mode: {mode}")

        return M


if __name__ == "__main__":
    pass
