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
import numpy as np
import pytest
import sisl

import grogupy
import grogupy._core
import grogupy._core.utilities

pytestmark = [pytest.mark.physics]


class TestPair:
    def test_generation(self):
        fdf = "./benchmarks/Fe3GeTe2/Fe3GeTe2.fdf"
        m1 = grogupy.MagneticEntity(fdf, 1, 2)
        m2 = grogupy.MagneticEntity(fdf, 2, 0)

        p = grogupy.Pair(m1, m2, [1, 2, 3])

        assert isinstance(p._dh, sisl.physics.Hamiltonian)

        assert isinstance(p.M1, grogupy.MagneticEntity)
        assert isinstance(p.M2, grogupy.MagneticEntity)
        assert m1 == p.M1
        assert m2 == p.M2

        assert np.allclose(p.supercell_shift, [1, 2, 3])

        assert p._Gij == []
        assert p._Gji == []
        assert p._Gij_tmp == []
        assert p._Gji_tmp == []

        assert p.energies == None
        assert p.J_iso == None
        assert p.J == None
        assert p.J_S == None
        assert p.D == None
        p.D

    def test_reset(self):
        pair = grogupy.load("./benchmarks/test_pair.pkl")

        pair._Gij = 1
        pair._Gji = None
        pair._Gij_tmp = np.array([10])
        pair._Gji_tmp = "[]"
        pair.energies = 3.14
        pair.J_iso = (10, 20, 30)
        pair.J = 2
        pair.J_S = (10, 20, 30)
        pair.D = 2

        pair.reset()
        assert pair._Gij == []
        assert pair._Gji == []
        assert pair._Gij_tmp == []
        assert pair._Gji_tmp == []
        assert pair.energies == None
        assert pair.J_iso == None
        assert pair.J == None
        assert pair.J_S == None
        assert pair.D == None

    @pytest.mark.xfail(raises=NotImplementedError)
    def test_add_G_tmp(self):
        raise NotImplementedError

    @pytest.mark.xfail(raises=NotImplementedError)
    def test_energies(self):
        raise NotImplementedError

    @pytest.mark.xfail(raises=NotImplementedError)
    def test_exchange(self):
        raise NotImplementedError

    def test_equality(self):
        p = grogupy.load("./benchmarks/test_pair.pkl")

        p2 = p.copy()
        assert p == p2

        p2._dh = sisl.get_sile("./benchmarks/Fe3GeTe2/Fe3GeTe2.fdf").read_hamiltonian()
        assert p != p2
        p2._dh = p._dh
        assert p == p2

        p2.M1 = grogupy.MagneticEntity("./benchmarks/Fe3GeTe2/Fe3GeTe2.fdf", atom=3)
        assert p != p2
        p2.M1 = p.M1
        assert p == p2

        p2.M2 = grogupy.MagneticEntity("./benchmarks/Fe3GeTe2/Fe3GeTe2.fdf", atom=4)
        assert p != p2
        p2.M2 = p.M2
        assert p == p2

        p2.supercell_shift = np.array([100, 100, 100, 100])
        assert p != p2
        p2.supercell_shift = p.supercell_shift
        assert p == p2

        p2._Gij = [np.zeros(3)]
        assert p != p2
        p2._Gij = p._Gij
        assert p == p2

        p2._Gji = None
        assert p != p2
        p2._Gji = p._Gji
        assert p == p2

        p2.energies = np.zeros(3)
        assert p != p2
        p2.energies = p.energies
        assert p == p2

        p2.J_iso = 100
        assert p != p2
        p2.J_iso = p.J_iso
        assert p == p2

        p2.J = np.zeros(3)
        assert p != p2
        p2.J = p.J
        assert p == p2

        p2.J_S = 1000 * np.ones(3)
        assert p != p2
        p2.J_S = p.J_S
        assert p == p2

        p2.D = 1000 * np.ones(3)
        assert p != p2
        p2.D = p.D
        assert p == p2

    @pytest.mark.parametrize("shift", [[0, 0, 0], [0, 1, 2], [-1, 10, 0]])
    @pytest.mark.parametrize(
        "atom, l, orb",
        [
            (None, None, 1),
            (None, None, [1]),
            (None, None, [1, 2]),
            (1, None, None),
            (1, None, 1),
            (1, None, [1]),
            (1, None, [1, 2]),
            (1, None, [[1, 2]]),
            (1, 1, None),
            (1, [1], None),
            (1, [1, 2], None),
            (1, [[1, 2]], None),
            ([1], None, None),
            ([1], None, 1),
            ([1], None, [1]),
            ([1], None, [1, 2]),
            ([1], None, [[1, 2]]),
            ([1], 1, None),
            ([1], [1], None),
            ([1], [1, 2], None),
            ([1], [[1, 2]], None),
            ([1, 2], None, None),
            ([1, 2], None, 1),
            ([1, 2], None, [1]),
            ([1, 2], None, [1, 2]),
            ([1, 2], None, [[1, 2], [1, 2]]),
            ([1, 2], 1, None),
            ([1, 2], [1], None),
            ([1, 2], [1, 2], None),
            ([1, 2], [[1, 2], [1, 2]], None),
            # tests fropdecipher
            ([0], None, [[1]]),
            ([0], None, [[1, 2]]),
            ([0], [[1]], None),
            ([0], [[1, 2]], None),
            ([0], [[None]], None),
            ([1], None, [[1]]),
            ([1], None, [[1, 2]]),
            ([1], [[1]], None),
            ([1], [[1, 2]], None),
            ([1], [[None]], None),
        ],
    )
    def test_copy(self, atom, l, orb, shift):
        m1 = grogupy.MagneticEntity(
            "./benchmarks/Fe3GeTe2/Fe3GeTe2.fdf",
            atom,
            l,
            orb,
        )
        m2 = grogupy.MagneticEntity(
            "./benchmarks/Fe3GeTe2/Fe3GeTe2.fdf",
            atom,
            l,
            orb,
        )
        p1 = grogupy.Pair(m1, m2)
        p2 = grogupy.Pair(m2, m1, shift)

        p1c = p1.copy()
        assert p1 == p1c
        p1c._Gji = 1
        assert p1 != p1c

        p2c = p2.copy()
        assert p2 == p2c
        p2c.energies = 1
        assert p2 != p2c

    def test_getstate_setstate(self):
        p = grogupy.load("./benchmarks/test_pair.pkl")

        state = p.__getstate__()
        assert isinstance(state, dict)

        p2 = object.__new__(grogupy.Pair)
        p2.__setstate__(state)
        assert p == p2


if __name__ == "__main__":
    pass
