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
import os
import subprocess

import pytest

pytestmark = [pytest.mark.cli]


class TestCommandLineTools:
    @pytest.mark.parametrize(
        "path",
        [
            "./src/grogupy/cli/tests/input1.py",
            "./src/grogupy/cli/tests/input2.py",
            "./src/grogupy/cli/tests/input3.py",
            "./src/grogupy/cli/tests/input4.py",
            "./src/grogupy/cli/tests/input5.py",
            "./src/grogupy/cli/tests/input6.py",
            "./src/grogupy/cli/tests/input0.fdf",
            "./src/grogupy/cli/tests/input1.fdf",
        ],
    )
    def test_run(self, path):
        subprocess.run(["grogupy_run", path])

        assert os.path.isfile("./src/grogupy/cli/tests/test.magnopy.txt")
        os.remove("./src/grogupy/cli/tests/test.magnopy.txt")
        assert os.path.isfile("./src/grogupy/cli/tests/test.pkl")
        os.remove("./src/grogupy/cli/tests/test.pkl")
        assert os.path.isdir("./src/grogupy/cli/tests/test_UppASD_output")
        assert os.path.isfile("./src/grogupy/cli/tests/test_UppASD_output/jfile")
        assert os.path.isfile("./src/grogupy/cli/tests/test_UppASD_output/momfile")
        assert os.path.isfile("./src/grogupy/cli/tests/test_UppASD_output/posfile")
        assert os.path.isfile("./src/grogupy/cli/tests/test_UppASD_output/cell.tmp.txt")
        os.remove("./src/grogupy/cli/tests/test_UppASD_output/jfile")
        os.remove("./src/grogupy/cli/tests/test_UppASD_output/momfile")
        os.remove("./src/grogupy/cli/tests/test_UppASD_output/posfile")
        os.remove("./src/grogupy/cli/tests/test_UppASD_output/cell.tmp.txt")
        os.rmdir("./src/grogupy/cli/tests/test_UppASD_output")

    def test_analyze(self):
        subprocess.run(["grogupy_run", "./src/grogupy/cli/tests/input5.py"])
        subprocess.run(["grogupy_analyze", "./src/grogupy/cli/tests/test.pkl"])

        assert os.path.isfile("./src/grogupy/cli/tests/test.analysis.html")
        os.remove("./src/grogupy/cli/tests/test.analysis.html")
        os.remove("./src/grogupy/cli/tests/test.pkl")

    def test_convergence(self):
        subprocess.run(["grogupy_run", "./src/grogupy/cli/tests/convergence1.py"])
        subprocess.run(["grogupy_run", "./src/grogupy/cli/tests/convergence2.py"])
        subprocess.run(
            [
                "grogupy_convergence",
                "-t",
                "kset",
                "-f",
                "'./src/grogupy/cli/tests/convergence1.pkl ./src/grogupy/cli/tests/convergence2.pkl'",
            ]
        )

        assert os.path.isfile("./grogupy_kset_convergence.html")
        os.remove("./grogupy_kset_convergence.html")
        os.remove("./src/grogupy/cli/tests/convergence1.pkl")
        os.remove("./src/grogupy/cli/tests/convergence2.pkl")


if __name__ == "__main__":
    pass
