# Parsing toolkit for Python
from lark import Lark


def test():
    with open("source_code.txt") as source_code:
        source_code = source_code.read()
    run_parser(source_code)


def run_parser(program):
    parse_tree = parser.parse(program)
    print(parse_tree.pretty())
    print(parse_tree)
    return parse_tree


with open("grammar.lark") as grammar:
    grammar = grammar.read()

parser = Lark(grammar)

if __name__ == '__main__':
    test()
