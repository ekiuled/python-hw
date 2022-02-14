from inspect import getsource

from .fibonacci import fibonacci
from .ast_plot import plot_ast


def plot_fibonacci(fname: str) -> None:
    source = getsource(fibonacci)
    plot_ast(source, fname)


if __name__ == '__main__':
    plot_fibonacci('artifacts/AST.png')
