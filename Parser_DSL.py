from lark import Lark


class ParserDSL:
    # class which contains the parser

    grammar = ''  # name
    program = ''  # name

    def __init__(self, grammar, program):
        """
            Constructor of the class
            :param grammar: input from .lark file
                The grammar on which the parser would run
            :param program: input from a .txt file
                the code which would be parsed
        """
        self.grammar = grammar
        self.program = program
        self.parser = Lark(grammar)

    def run_parser(self):
        """
            Function to run the parser
                :return: lark tree. The result after parsing
        """
        parse_tree = self.parser.parse(self.program)

        return parse_tree
