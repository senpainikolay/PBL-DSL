
        
import Errors     
import Tokens



#
### CONSTANTS
# 

import string

LETTERS = string.ascii_letters
DIGITS = '0123456789' 
LETTERS_DIGITS = LETTERS + DIGITS


 

#
### TOKENS
#

TT_INT = 'TT_INT'
TT_FLOAT = 'FLOAT'
TT_PLUS = 'PLUS'
TT_MINUS = 'MINUS'
TT_MUL = 'MUL'
TT_DIV = 'DIV' 
TT_LPAREN = 'LPAREN' 
TT_RPAREN = 'RPAREN'  
TT_EOF = 'EOF' 

TT_LBRACKET = 'LBRACKET'
TT_RBRACKET = 'RBRACKET'

TT_INDENTIFIER = 'INDENTIFIER'
TT_KEYWORD = 'KEYWORD' 
TT_EQ = 'EQ'   

TT_COMMA = 'COMMA'

TT_NEWLINE = 'NEWLINE'

TT_PHOTO = 'PHOTO' 
TT_PERCENT = '%'

KEYWORDS = [ 
    'VAR',  
    'extract',
    'from',
    'compute', 
    "mean",
    "stdev",
     "max",
    "min",
    "median",
     "sum", 
    'on', 
    'each',
    'rows',
    'to',
    'barplot', 
    'countplot', 
    'scatterplot', 
    'displot',
    'countplot', 
    'show'
]

class Token:
    def __init__(self,type_, value = None):
        self.type = type_
        self.value = value
    
    def __repr__(self):
        if self.value: return f'{self.type} : {self.value}'
        return f'{self.type}' 
    
    def matches(self, type_, value):
        return self.type == type_ and self.value == value
    
#
### LEXER
# 

class Lexer:
    def __init__(self,text):
        self.text = text
        self.pos = -1
        self.current_char = None
        self.advance()
        
    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None
    
    def make_tokens(self):
        tokens = list()
        
        while self.current_char != None:
            if self.current_char in '  \t':
                self.advance() 
                
            elif self.current_char in ';\n':
                tokens.append(Token(TT_NEWLINE))
                self.advance()  
                
            elif self.current_char in LETTERS:
                tokens.append(self.make_identifier())
                
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())                 
                
                
            elif self.current_char == '+':
                tokens.append(Token(TT_PLUS))
                self.advance()  
                
            elif self.current_char == ',':
                tokens.append(Token(TT_COMMA))
                self.advance() 
                
            elif self.current_char == '-':
                tokens.append(Token(TT_MINUS))
                self.advance() 
            elif self.current_char == '*':
                tokens.append(Token(TT_MUL))
                self.advance() 
            elif self.current_char == '/':
                tokens.append(Token(TT_DIV))
                self.advance() 
            
            elif self.current_char == '%':
                tokens.append(Token(TT_PERCENT))
                self.advance() 
                
            elif self.current_char == '(':
                tokens.append(Token(TT_LPAREN))
                self.advance() 
            elif self.current_char == ')':
                tokens.append(Token(TT_RPAREN))
                self.advance()  
                
            elif self.current_char == '[':
                tokens.append(Token(TT_LBRACKET))
                self.advance() 
            elif self.current_char == ']':
                tokens.append(Token(TT_RBRACKET))
                self.advance()  
                
            elif self.current_char == '=':
                tokens.append(Token(TT_EQ))
                self.advance() 
            else:
                char = self.current_char
                self.advance()
                return [], IllegalCharError("'" + char + "'")
            
            
        tokens.append(Token(TT_EOF))
        return tokens, None
    
    def make_number(self):
        num_str =''
        dot_count = 0
        
        while self.current_char != None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1:
                    print("ERROR: INVALID FLOAT") 
                    break
                dot_count +=1 
                num_str += '.'
            
            else:
                num_str += self.current_char 
            
            self.advance()
        
        if dot_count == 0:
            return Token(TT_INT, int(num_str))
        else:
            return Token(TT_FLOAT, float(num_str))   
        
    
    def make_identifier(self):
        id_str = ''
        
        dot_count = 0
        
        while self.current_char != None and self.current_char in LETTERS_DIGITS + '_' + '.':
            if self.current_char == '.':
                if dot_count == 1:
                    print("ERROR: INVALID PHOTO FORMAT! 2 DOTS!") 
                    break
                dot_count +=1 
                self.advance()
                photo_format = '.'
                while self.current_char != None and self.current_char in LETTERS:
                    photo_format += self.current_char 
                    self.advance() 
                    
                if len(photo_format) > 4: 
                    print("INVALID PHOTO FORMAT, PLEASE USE ONLY J.jpg or .png")
                    break
        
                id_str += photo_format
                return Token(TT_PHOTO, id_str)
            
            else:
                id_str += self.current_char 
                self.advance()  
            

        tok_type = TT_KEYWORD if id_str in KEYWORDS else TT_INDENTIFIER
        return Token(tok_type, id_str) 




#
### ERRORS
#

class Error:
    def __init__(self,error_name,details):
        self.error_name = error_name
        self.details = details
        
    def as_string(self):
        result = f'{self.error_name} : {self.details}'
        return result

class IllegalCharError(Error):
    def __init__(self, details):
        super().__init__('Illegal Character',details)  
        

class InvalidSynthaxError(Error):
    def __init__(self, details):
        super().__init__('Illegal Synthax ',details)   
        
        

class ExpectedSymbolError(Error):
    def __init__(self, details):
        super().__init__('Expected Symbol ',details)  
        
class ExpectedIdentError(Error):
    def __init__(self, details):
        super().__init__('Expected Ident  ',details) 