import numpy as np
from numbers import Number
from typing import List

class WriteToFileMixin:
    def write_to_file(self, file_name):
        with open(file_name, "w") as fout:
            print(self, file=fout)

class ToStringMixin:
    def __repr__(self):
        return '\n'.join(list(map(lambda x: ' '.join(map(str, x)), self._data)))

class GetSetMixin:

    @property
    def data(self):
        return self._data
    
    @property
    def rows(self):
        return self._rows

    @property
    def cols(self):
        return self._cols

    @data.setter
    def data(self, array):
        self._data = array

class MixinMatrix(np.lib.mixins.NDArrayOperatorsMixin, ToStringMixin, WriteToFileMixin, GetSetMixin):

    def __init__(self, array: List[List[int]]):
        self._rows = len(array)
        self._cols = len(array[0])
        for row in array:
            if self._cols != len(row):
                raise Exception("Matrix rows should have the same size")
        self._data = np.asarray(array)

    _HANDLED_TYPES = (np.ndarray, Number)

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        out = kwargs.get('out', ())
        for x in inputs + out:
            if not isinstance(x, self._HANDLED_TYPES + (MixinMatrix,)):
                return NotImplemented

        inputs = tuple(x._data if isinstance(x, MixinMatrix) else x
                       for x in inputs)
        if out:
            kwargs['out'] = tuple(
                x._data if isinstance(x, MixinMatrix) else x
                for x in out)
        result = getattr(ufunc, method)(*inputs, **kwargs)

        if type(result) is tuple:
            return tuple(type(self)(x) for x in result)
        elif method == 'at':
            return None
        else:
            return type(self)(result)

if __name__ == '__main__':
    np.random.seed(0)
    a = MixinMatrix(np.random.randint(0, 10, (10, 10)))
    b = MixinMatrix(np.random.randint(0, 10, (10, 10)))
    (a + b).write_to_file('artifacts/medium/matrix+.txt')
    (a * b).write_to_file('artifacts/medium/matrix*.txt')
    (a @ b).write_to_file('artifacts/medium/matrix@.txt')