from typing import Any

from inspect import getsource
from ast import parse, unparse, NodeVisitor, AST

import pygraphviz as pvg

from fibonacci import fibonacci


class Visitor(NodeVisitor):
    def __init__(self):
        self.graph = pvg.AGraph()
        self.path = []
        self.count = 0

    def generic_visit(self, node: AST) -> Any:
        self.count = id = self.count + 1
        name = f'{type(node).__name__}\n{unparse(node)}'
        self.graph.add_node(id, label=name, shape='box', fontname='JetBrains Mono')

        if self.path:
            parent = self.path[-1]
            self.graph.add_edge(parent, id)

        self.path.append(id)
        super().generic_visit(node)
        self.path.pop()

    def build(self) -> pvg.AGraph:
        self.graph.layout(prog='dot')
        return self.graph


def plot_ast(source: str, fname: str) -> None:
    ast = parse(source)

    visitor = Visitor()
    visitor.visit(ast)
    visitor.build().draw(fname)


if __name__ == '__main__':
    source = getsource(fibonacci)
    plot_ast(source, 'artifacts/AST.png')
