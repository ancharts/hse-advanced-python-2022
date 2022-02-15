def generate_latex(filename):
    def make_header():
        return '\documentclass{article}\n' + '\\usepackage{graphicx}\n' + '\\begin{document}\n'

    def get_table(filename):
        return list(map(lambda x: x.split(), open(filename, 'r').readlines()))

    def make_final():
        return '\\end{document}'

    return make_header() + '\t\\begin{tabular}{|' + '|'.join(
        ['c'] * len(get_table(filename)[0])) + '|}\n' + '\t\t\\hline\n' + "".join(
        list(map(lambda x: '\t\t' + ' & '.join(x) + ' \\\\\n\t\t\hline\n',
                 get_table(filename)))) + '\t\\end{tabular}\n' + '\n\t\\includegraphics[height=10cm]{ast.png}\n' + make_final()


if __name__ == '__main__':
    print(generate_latex('table.txt'), file=open('tableout.txt', 'w'))
