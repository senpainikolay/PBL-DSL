
from Interpreter import Interpreter
from  Lexer import Lexer
from  Parser import Parser  



def run_lexer_parser(text):
        lexer = Lexer(text)
        tokens, error = lexer.make_tokens() 
        if error: return None, error
        
        #Generate AST
        print(tokens)
        parser = Parser(tokens)
        ast = parser.parse() 
        
        return ast 


def start():

    text = open("new.txt", "r").read()

    result = run_lexer_parser(text)
    if result.error:
        print(result.error.as_string()) 
        return 
    else:
        print(result.node)  
    #print(result) 
    interpreter = Interpreter()

    res,next_statement = interpreter.visit(result.node)
    if res.error:
        print(res.error)
        return
    while next_statement:
        res,next_statement =  interpreter.visit(next_statement) 
        if res.error:
            print(res.error) 
            return 

    #print(interpreter.symbol_table.symbols) 


start()


    
        