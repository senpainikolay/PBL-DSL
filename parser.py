# Parsing toolkit for Python
from lark import Lark


def test():
    text = """
              a = extract [name, age, xx] from image [xyz.jpg]  
              b = compute mean on a[name, xx]
              m = compute mean on a[each 12 rows]
              n = 30 percent [20 to 60] rows a
              lmplot a, x = name, y = age
              save a as csv
            """
    run_parser(text)


def run_parser(program):
    parse_tree = parser.parse(program)
    print(parse_tree.pretty())


with open("grammar.lark") as grammar:
    grammar = grammar.read()

parser = Lark(grammar)

if __name__ == '__main__':
    test()
