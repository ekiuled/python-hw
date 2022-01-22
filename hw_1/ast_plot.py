from typing import Any

from inspect import getsource
import ast
import pygraphviz as pvg

from fibonacci import fibonacci


class Visitor(ast.NodeVisitor):
    def __init__(self):
        self.graph = pvg.AGraph()
        self.path = []
        self.count = 0

    def generic_visit(self, node: ast.AST, color: str = 'lightblue', show_value: bool = False) -> Any:
        self.count = id = self.count + 1
        value = ast.unparse(node) if show_value else ''
        name = f'{type(node).__name__}\n{value}'

        self.graph.add_node(id, label=name, shape='box', fontname='JetBrains Mono', fillcolor=color, style='filled')

        if self.path:
            parent = self.path[-1]
            self.graph.add_edge(parent, id)

        self.path.append(id)
        super().generic_visit(node)
        self.path.pop()

    def _visit_literal(self, node: ast.AST) -> Any:
        self.generic_visit(node, color='lightyellow', show_value=True)

    def _visit_variable(self, node: ast.AST) -> Any:
        self.generic_visit(node, color='lightgreen', show_value=True)

    def _visit_operator(self, node: ast.AST) -> Any:
        self.generic_visit(node, color='plum')

    def _visit_call(self, node: ast.AST) -> Any:
        self.generic_visit(node, color='gold')

    def _visit_control_flow(self, node: ast.AST) -> Any:
        self.generic_visit(node, color='lightslateblue')

    def visit_Constant(self, node: ast.Constant) -> Any:
        self._visit_literal(node)

    def visit_List(self, node: ast.List) -> Any:
        self._visit_literal(node)

    def visit_Name(self, node: ast.Name) -> Any:
        self._visit_variable(node)

    def visit_arg(self, node: ast.arg) -> Any:
        self._visit_variable(node)

    def visit_BinOp(self, node: ast.BinOp) -> Any:
        self._visit_operator(node)

    def visit_UnaryOp(self, node: ast.UnaryOp) -> Any:
        self._visit_operator(node)

    def visit_Assign(self, node: ast.Assign) -> Any:
        self._visit_operator(node)

    def visit_Call(self, node: ast.Call) -> Any:
        self._visit_call(node)

    def visit_For(self, node: ast.For) -> Any:
        self._visit_control_flow(node)

    def visit_Return(self, node: ast.Return) -> Any:
        self._visit_control_flow(node)

    def build(self) -> pvg.AGraph:
        self.graph.layout(prog='dot')
        return self.graph


def plot_ast(source: str, fname: str) -> None:
    AST = ast.parse(source)
    visitor = Visitor()
    visitor.visit(AST)
    visitor.build().draw(fname)


if __name__ == '__main__':
    source = getsource(fibonacci)
    plot_ast(source, 'artifacts/AST.png')
