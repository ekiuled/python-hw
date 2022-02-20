from __future__ import annotations
import numpy as np


class SizeMismatch(Exception):
    """Raised when matrix sizes don't match for an operaton"""

    def __init__(self, n1: int, m1: int, n2: int, m2: int):
        self.message = f'Matrix size mismatch: [{n1}x{m1}] and [{n2}x{m2}]'
        super().__init__(self.message)


class Matrix:
    @classmethod
    def random(cls, low: int, high: int, n: int, m: int) -> Matrix:
        return Matrix(np.random.randint(low, high, (n, m)).tolist())

    def __init__(self, values: list[list]):
        self.values = values
        self.n = len(values)
        self.m = len(values[0])

    def __repr__(self) -> str:
        return f'{type(self).__name__}({repr(self.values)})'

    def __str__(self) -> str:
        return '\n'.join(['\t'.join(map(str, row)) for row in self.values])

    def __add__(self, other: Matrix) -> Matrix:
        if self.n != other.n or self.m != other.m:
            raise SizeMismatch(self.n, self.m, other.n, other.m)
        return Matrix([[x1 + x2 for x1, x2 in zip(row1, row2)]
                       for row1, row2 in zip(self.values, other.values)])

    def __mul__(self, other: Matrix) -> Matrix:
        if self.n != other.n or self.m != other.m:
            raise SizeMismatch(self.n, self.m, other.n, other.m)
        return Matrix([[x1 * x2 for x1, x2 in zip(row1, row2)]
                       for row1, row2 in zip(self.values, other.values)])

    def __matmul__(self, other: Matrix) -> Matrix:
        if self.m != other.n:
            raise SizeMismatch(self.n, self.m, other.n, other.m)
        return Matrix([[sum([self.values[i][k] * other.values[k][j] for k in range(self.m)])
                        for j in range(other.m)]
                       for i in range(self.n)])


if __name__ == '__main__':
    np.random.seed(0)
    a = Matrix.random(0, 10, 10, 10)
    b = Matrix.random(0, 10, 10, 10)

    with open('artifacts/easy/matrix+.txt', 'w') as file:
        file.write(str(a + b))
    with open('artifacts/easy/matrix*.txt', 'w') as file:
        file.write(str(a * b))
    with open('artifacts/easy/matrix@.txt', 'w') as file:
        file.write(str(a @ b))
