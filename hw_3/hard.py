from attr import has
from easy import Matrix


class HashMixin:
    """Хэш-функция для матриц: сумма всех элементов"""

    def __hash__(self) -> int:
        return sum(map(sum, self.values))


class HashedMatrix(HashMixin, Matrix):
    pass


class MatmulCachedMatrix(HashedMatrix):
    cache = {}

    def __matmul__(self, other):
        key = (hash(self), hash(other))
        if key not in self.cache:
            self.cache[key] = super().__matmul__(other)
        return self.cache[key]


if __name__ == '__main__':
    a = HashedMatrix([[0, 0], [0, 0]])
    c = HashedMatrix([[1, 0], [0, -1]])
    b = d = HashedMatrix([[1, 0], [0, 1]])

    with open('artifacts/hard/A.txt', 'w') as file:
        file.write(str(a))
    with open('artifacts/hard/B.txt', 'w') as file:
        file.write(str(b))
    with open('artifacts/hard/C.txt', 'w') as file:
        file.write(str(c))
    with open('artifacts/hard/D.txt', 'w') as file:
        file.write(str(d))

    with open('artifacts/hard/AB.txt', 'w') as file:
        file.write(str(a @ b))
    with open('artifacts/hard/CD.txt', 'w') as file:
        file.write(str(c @ d))
    with open('artifacts/hard/hash.txt', 'w') as file:
        file.write(f'AB {hash(a @ b)}\n')
        file.write(f'CD {hash(c @ d)}\n')
