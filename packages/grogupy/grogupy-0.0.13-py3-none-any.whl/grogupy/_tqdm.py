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
from .config import CONFIG

# if tqdm is requested
if CONFIG.tqdm_requested:
    # tqdm might not work, but this should not be a problem
    try:
        from tqdm.autonotebook import tqdm

        class _tqdm:
            def __init__(self, iterable, head_node=True, **kwargs):
                self.head_node = head_node

                self.iterable = iterable
                self.tqdm = tqdm(iterable, **kwargs)

            def __iter__(self):
                if CONFIG.is_CPU:
                    from mpi4py import MPI

                    if self.head_node:
                        if MPI.COMM_WORLD.rank == 0:
                            return iter(self.tqdm)
                        else:
                            return iter(self.iterable)
                    else:
                        return iter(self.tqdm)

                elif CONFIG.is_GPU:
                    return iter(self.tqdm)
                else:
                    raise Exception("Unknown architecture, use CPU or GPU!")

            def __call__(self):
                if CONFIG.is_CPU:
                    from mpi4py import MPI

                    if self.head_node:
                        if MPI.COMM_WORLD.rank == 0:
                            return self.tqdm
                        else:
                            return self.iterable
                    else:
                        return self.tqdm

                elif CONFIG.is_GPU:
                    return self.tqdm
                else:
                    raise Exception("Unknown architecture, use CPU or GPU!")

            def update(self, **kwargs):
                self.tqdm.update(**kwargs)

    except:
        print("Please install tqdm for nice progress bar.")

        class _tqdm:
            def __init__(self, iterable, head_node=True, **kwargs):
                self.iterable = iterable

            def __iter__(self):
                return iter(self.iterable)

            def __call__(self):
                return self.iterable

            def update(self, **kwargs):
                pass


# if tqdm is not requested it will be a dummy wrapper function
else:

    class _tqdm:
        def __init__(self, iterable, head_node=True, **kwargs):
            self.iterable = iterable

        def __iter__(self):
            return iter(self.iterable)

        def __call__(self):
            return self.iterable

        def update(self, **kwargs):
            pass


if __name__ == "__main__":
    pass
