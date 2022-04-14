from Parser_DSL import ParserDSL
from Interpreter import Interpreter
import warnings

# The grammar of the DSL
with open("grammar.lark") as grammar:
    grammar = grammar.read()

# The program given for execution
with open("source_code.txt") as source_code:
    source_code = source_code.read()

# generating the parse tree
Parser = ParserDSL(grammar, source_code)
tree = Parser.run_parser()

# executing the code
Interpreter = Interpreter(tree)
Interpreter.run_interpreter()