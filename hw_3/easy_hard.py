import copy
import numpy as np
from typing import List

class Matrix:

    def __init__(self, array: List[List[int]]):
        self._rows = len(array)
        self._cols = len(array[0])

        for row in array:
            if self._cols != len(row):
                raise Exception("Matrix rows should have the same size")

        self._data = array

    def __add__(self, other: 'Matrix') -> 'Matrix':
        if self._rows != other._rows or self._cols != other._cols:
            raise Exception("Incorrect dimensions for matrix addition")

        res = copy.deepcopy(self._data)
        for i in range(self._rows):
            for j in range(self._cols):
                res[i][j] += other._data[i][j]
        return Matrix(res)

    def __mul__(self, other: 'Matrix') -> 'Matrix':
        if self._rows != other._rows or self._cols != other._cols:
            raise Exception("Incorrect dimensions for matrix component multiplication")

        res = copy.deepcopy(self._data)
        for i in range(self._rows):
            for j in range(self._cols):
                res[i][j] *= other._data[i][j]
        return Matrix(res)

    def __matmul__(self, other):
        if self._cols != other._rows:
            raise Exception("Incorrect dimensions for matrix multiplication")

        res = [[0]*self._rows for i in range(other._cols)]
        for i in range(self._rows):
            for j in range(other._cols):
                for k in range(self._cols):
                    res[i][j] += (self._data[i][k] * other._data[k][j])
        return Matrix(res)

    def __repr__(self):
        return '\n'.join(list(map(lambda x: ' '.join(map(str, x)), self._data)))


class HashableMatrix(Matrix):
    saved = {}

    def __hash__(self: 'Matrix') -> int:
        return int(sum([sum(row) for row in self._data]))

    def __matmul__(self, other):
        a = hash(self)
        b = hash(other)
        key = (hash(self), hash(other))
        if key in self.saved:
            return self.saved[key]
        res = HashableMatrix(super().__matmul__(other)._data)
        self.saved[key] = res
        return res

    @classmethod
    def clear(self):
        self.saved = {}

def find_collision():
    HashableMatrix.clear()
    while True:
        a = HashableMatrix(np.random.randint(0, 10, (3, 3)))
        b = HashableMatrix(np.random.randint(0, 10, (3, 3)))
        c = HashableMatrix(np.random.randint(0, 10, (3, 3)))
        d = b
        ab = a @ b
        HashableMatrix.clear()
        cd = c @ d
        HashableMatrix.clear()
        if hash(a) == hash(c) and (a != c) and (ab != cd):
            with open('artifacts/hard/A.txt', 'w') as fout:
                print(a, file=fout)
            with open('artifacts/hard/B.txt', 'w') as fout:
                print(b, file=fout)
            with open('artifacts/hard/C.txt', 'w') as fout:
                print(c, file=fout)
            with open('artifacts/hard/D.txt', 'w') as fout:
                print(d, file=fout)
            with open('artifacts/hard/AB.txt', 'w') as fout:
                print(ab, file=fout)
            with open('artifacts/hard/CD.txt', 'w') as fout:
                print(cd, file=fout)
            with open('artifacts/hard/hash.txt', 'w') as fout:
                print(f"Hash A @ B = {hash(ab)}, hash C @ D = {hash(cd)}", file=fout)
            break

if __name__ == '__main__':

    np.random.seed(0)
    a = Matrix(np.random.randint(0, 10, (10, 10)))
    b = Matrix(np.random.randint(0, 10, (10, 10)))
    with open('artifacts/easy/matrix+.txt', 'w') as fout:
        print(a+b, file=fout)
    with open('artifacts/easy/matrix*.txt', 'w') as fout:
        print(a*b, file=fout)
    with open('artifacts/easy/matrix@.txt', 'w') as fout:
        print(a@b, file=fout)

    find_collision()

