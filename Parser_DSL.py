from lark import Lark


class ParserDSL:
    grammar = ''  # name
    program = ''  # name

    def __init__(self, grammar, program):
        self.grammar = grammar
        self.program = program
        self.parser = Lark(grammar)

    def run_parser(self):
        parse_tree = self.parser.parse(self.program)
        print(parse_tree.pretty())

        return parse_tree
