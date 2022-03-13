from lark import Lark

pbl_grammar =  """ 

start: set_of_affirmations+ 

set_of_affirmations: affirmation
                    | set_of_affirmations affirmation*

affirmation: assigment 
           | plot 
           | save   

assigment: variable "=" data_extraction 
         | variable "=" computation 

plot: IMPLOT df
    | SCATTERPLOT df 
    | DISPLOT df
    | BARPLOT df
    | COUNTPLOT  df

data_extraction: "extract" string_list "from" image 
                | "extract" string_list "from" folder 

computation: COMPUTE measure "on" df "[" "each" INT "rows" "]"  | COMPUTE measure "on" variable 
            | num "percent" range "rows" df 

save:  "save" df "as" format  

image: "image" string 

folder: "folder" string 

measure: WORD

format: "csv" | "xls" 

df:  variable 
   | variable string_list 

range: "[" INT "to" INT  "]" 
     | "[" INT "]"

string_list:  "[" string_items  "]" 

string_items: string 
            | string string_items 

string: "["WORD"]"   |  "[" IMG_FILE "]" | WORD

variable: CNAME   

num: FLOAT   


COMPUTE: "compute" 

IMG_FILE: WORD "." WORD

IMPLOT : "implot"  
SCATTERPLOT: "scatterplot"
DISPLOT: "displot"
BARPLOT: "barplot"
COUNTPLOT: "countplot"

%import common.LETTER
%import common.INT   
%import common.CNAME   
%import common.WORD
%import common.FLOAT
%import common.WS
%ignore WS
"""


parser = Lark(pbl_grammar)   

def test(): 

 
    text = """
  a = extract [name] from image [xyz.jpg]  
  b = compute mean on a
   save a as csv
    """ 
    run_parser(text) 

def run_parser(program):
    parse_tree = parser.parse(program)  
    print(parse_tree)



if __name__ == '__main__':
    test()