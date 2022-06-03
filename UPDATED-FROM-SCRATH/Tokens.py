
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