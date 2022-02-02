import ast
import graphviz

graph = graphviz.Graph()
nodes = 0
colors = {'op': '#AE431E', 'arg': '#8A8635', 'fun': '#D06224'}


class Visitor(object):
    def visit(self, node):
        global nodes
        curr, nodes = nodes, nodes + 1
        res = style(node)
        graph.node(str(curr), label=res[0], fillcolor=res[1], shape=res[2], style='filled')

        for field, value in ast.iter_fields(node):
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, ast.AST):
                        graph.edge(str(curr), str(self.visit(item)))
            elif isinstance(value, ast.AST):
                graph.edge(str(curr), str(self.visit(value)))
        return curr


def style(node: ast.AST):
    label = node.__class__.__name__
    color = "#f39c12"
    shape = 'square'
    if isinstance(node, ast.Constant):
        label = f"Constant = {node.value}"
        color = colors['arg']
        shape = 'round'
    elif isinstance(node, ast.Name):
        label = f"Name = {node.id}"
        color = colors['arg']
        shape = 'round'
    elif isinstance(node, ast.BoolOp):
        color = colors['op']
        shape = 'round'
    elif isinstance(node, ast.BinOp):
        color = colors['op']
        shape = 'round'
    elif isinstance(node, ast.Or):
        label = 'Or'
        color = colors['op']
        shape = 'circle'
    elif isinstance(node, ast.Eq):
        label = '=='
        color = colors['op']
        shape = 'circle'
    elif isinstance(node, ast.Sub):
        label = "-"
        color = colors['op']
        shape = 'circle'
    elif isinstance(node, ast.Add):
        label = "+"
        color = colors['op']
        shape = 'circle'
    elif isinstance(node, ast.FunctionDef):
        label = f"Func {node.name}"
        color = colors['fun']
    elif isinstance(node, ast.arg):
        label = f"Arg = {node.arg}"
        color = colors['arg']
        shape = 'round'
    return (label, color, shape)


def print_ast():
    with open('easy.py', 'r') as fin:
        code = "".join(fin.readlines())
    obj = ast.parse(code)
    x = Visitor()
    x.visit(obj)
    graph.render('artifacts/ast.graph')


if __name__ == '__main__':
    print_ast()
