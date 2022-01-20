from typing import Any

from inspect import getsource
from ast import parse, unparse, NodeVisitor, AST

import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
import matplotlib.pyplot as plt

from fibonacci import fibonacci


class Visitor(NodeVisitor):
    def __init__(self):
        self.graph = nx.Graph()
        self.labels = {}
        self.path = []
        self.count = 0

    def generic_visit(self, node: AST) -> Any:
        self.count = id = self.count + 1
        name = f'{type(node).__name__}\n{unparse(node)}'
        self.labels[id] = name

        if self.path:
            parent = self.path[-1]
            self.graph.add_edge(parent, id)

        self.path.append(id)
        super().generic_visit(node)
        self.path.pop()


def plot_ast(source: str, fname: str) -> None:
    ast = parse(source)

    visitor = Visitor()
    visitor.visit(ast)
    G = visitor.graph
    pos = graphviz_layout(G, prog='dot')

    plt.figure(figsize=(10, 10))
    nx.draw(G, pos)
    nx.draw_networkx_labels(G, pos, visitor.labels)

    plt.savefig(fname)


if __name__ == '__main__':
    source = getsource(fibonacci)
    plot_ast(source, 'artifacts/AST.png')
