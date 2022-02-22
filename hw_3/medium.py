import numpy as np


class ArithmeticMixin(np.lib.mixins.NDArrayOperatorsMixin):
    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        for input in inputs:
            if not isinstance(input, type(self)):
                return NotImplemented
        inputs = (input.values for input in inputs)
        return type(self)(getattr(ufunc, method)(*inputs, **kwargs))


class FileWriteMixin:
    def write_to_file(self, filename):
        with open(filename, 'w') as file:
            file.write(str(self))


class StrMixin:
    def __str__(self):
        return '\n'.join(['\t'.join(map(str, row)) for row in self.values])

    def __repr__(self) -> str:
        return f'{type(self).__name__}({repr(self.values)})'


class ValuesMixin:
    def __init__(self, values):
        self.values = values

    @property
    def values(self):
        return self._values

    @values.setter
    def values(self, value):
        self._values = value


class Matrix(ArithmeticMixin, FileWriteMixin, StrMixin, ValuesMixin):
    pass


if __name__ == '__main__':
    np.random.seed(0)
    a = Matrix(np.random.randint(0, 10, (10, 10)))
    b = Matrix(np.random.randint(0, 10, (10, 10)))

    (a + b).write_to_file('artifacts/medium/matrix+.txt')
    (a * b).write_to_file('artifacts/medium/matrix*.txt')
    (a @ b).write_to_file('artifacts/medium/matrix@.txt')
