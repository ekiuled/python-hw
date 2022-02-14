from astplot.plot_fibonacci import plot_fibonacci


def latex_row_curried(columns: int):
    def latex_row(row: list) -> str:
        missing_columns = columns - len(row)
        return f'{" & ".join(map(str, row))}{" & " * missing_columns} \\\\ \\hline'
    return latex_row


def latex_table(table: list[list]) -> str:
    column_amount = max(map(len, table))
    if not column_amount:
        return ''

    columns = 'l|' * column_amount
    preamble = [f'\\begin{{tabular}}{{|{columns}}}', '\\hline']
    epilogue = ['\\end{tabular} \\\\']
    contents = list(map(latex_row_curried(column_amount), table))
    return '\n'.join(preamble + contents + epilogue)


def latex_image(filepath: str) -> str:
    return f'\\includegraphics[width=\\textwidth]{{{filepath}}} \\\\'


def latex(contents: list[str]):
    preamble = ['\\documentclass{article}', '\\usepackage{graphicx}', '\\begin{document}']
    epilogue = ['\\end{document}']
    return '\n'.join(preamble + contents + epilogue)


if __name__ == '__main__':
    table = [['Hello', ',', 'world', '!'],
             [1, 2, 3],
             [4, 5],
             [6, 7, 8, 9],
             [3.14]]

    image = 'AST.png'
    plot_fibonacci(f'artifacts/{image}')

    with open('artifacts/example.tex', 'w') as tex:
        tex.write(latex([
            latex_table(table),
            latex_image(image)
        ]))
