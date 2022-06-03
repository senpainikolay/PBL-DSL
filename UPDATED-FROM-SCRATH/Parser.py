
# 
### NODES 
# 
        
class VarAssignNode:
    def __init__(self, var_name_tok, value_node):
        self.var_name_tok = var_name_tok
        self.node_name = 'ASSIGN'
        self.value_node = value_node
    
    def __repr__(self): 
        return f'({self.var_name_tok}, {self.node_name},{self.value_node})'
    
    
    
    
    
class PercentNode:
     def __init__(self,nr):
        self.nr = nr
        self.nr.type = 'Percentage'
    
     def __repr__(self):
        return f'{self.nr}'
                
        

class DataframeAccessNode:
    def __init__(self, arr_name, colNode = None , rowNode = None ):
        self.name = arr_name 
        self.name.type = 'Dataframe'
        self.colNode = colNode 
        self.rowNode = rowNode
    
    def __repr__(self):
        if self.colNode and self.rowNode:
            return f'( {self.name}, {self.colNode}, {self.rowNode})'
        elif self.colNode and  self.rowNode == None:
            return f'( {self.name}, {self.colNode})'
        elif self.rowNode and  self.colNode == None:
            return f'( {self.name}, {self.rowNode})'
        else:
            return f'({self.name})' 
        
class ColumnNode:
    def __init__(self, val, right = None):
        self.val = val 
        self.val.type = 'Column'
        self.right = right
        
    def __repr__(self):
        if self.right == None:
            return f'({self.val})'
        return f'({self.val}, {self.right})'   
    
    

        
class StatementNode:
    def __init__(self, val, right = None):
        self.val = val 
        self.right = right
        
    def __repr__(self):
        if self.right == None:
            return f'(Statement, {self.val})'
        return f'(Statement, {self.val}, {self.right})'  
    
    

class ExtractionNode:
    def __init__(self, cols, source):
        self.cols = cols 
        self.source = source
        
    def __repr__(self):
        return f'(Extraction_call, {self.cols}, {self.source})' 
    
    

    
class ComputeNode:
    def __init__(self, dataframe, method ):
        self.name = 'Compute'
        self.method = MethodNode(method)
        self.dataframe = dataframe
    
    def __repr__(self):
        return f'( {self.name}, {self.dataframe}, {self.method})'  
    
    
class MethodNode:
    def __init__(self,method_tok):
        self.method = method_tok
        self.method.type = 'Method'
    
    def __repr__(self):
        return f'({self.method})' 
    


class RowNode:
    def __init__(self,nr1, nr2 = None, each_bool = None):
        self.each_bool = each_bool
        if self.each_bool:
            self.nr1 = EachNode(nr1)
            self.nr2 = nr2 
        else:
            self.nr1 = nr1
            self.nr2 = nr2 
            
        if nr2:
            self.nr2 = ToNode(nr2)
        
        self.nr1.type = 'RowIndex'
        
    def __repr__(self):
        if self.each_bool == None and self.nr2:
            return f'({self.nr1}, {self.nr2})'
        return f'({self.nr1})'                
    
    
class ToNode:
    def __init__(self,val):
        self.val = val
        self.val.type = 'TO'
    
    def __repr__(self):
        return f'({self.val})' 
     

class EachNode:
    def __init__(self,val):
        self.val = val
        self.val.type = 'Each'
    
    def __repr__(self):
        return f'{self.val}' 


class ShowNode:
    def __init__(self,val):
        self.val = val
        self.val.type = 'Show'
    
    def __repr__(self):
        return f'{self.val}'


class PlotNode:
    def __init__(self,type, df, x,y = None):
        self.type = type
        self.df = df 
        self.x = x 
        self.y = y 

    def __repr__(self):
        return f'( PLOT, {self.type}, {self.df}, {self.x}, {self.y}) '



############## 
# PARSER RESULTS #

class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None
        
    def register(self,res):
        if isinstance(res,ParseResult):
            if res.error: self.error = res.error
            return res.node
        
        return res    
    
    def success(self,node):
        self.node = node
        return self
    
    def failure(self, error):
        self.error = error
        return self
        
        
        
             

#
### PARSER
# 


class Parser:
    def __init__(self,tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.advance()
        
    def advance(self):
        self.tok_idx +=1 
        if self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]
        
        return self.current_tok  
    
    def parse(self):
        res = self.stat()
        if not res.error and self.current_tok.type != TT_EOF:
            return res.failure(InvalidSynthaxError(f'Smth wrong around {self.current_tok}'))
        return res
    
    
    
    def stat(self):
        res = ParseResult()
        while self.current_tok.type == TT_NEWLINE:
            res.register(self.advance())
            
        left = res.register(self.expr())
        
        if res.error: return res
        right = self.rec_stat()
        if res.error: return res
        
        return res.success(StatementNode(left,right))
    
    def rec_stat(self):
        res = ParseResult()
        
        while self.current_tok.type == TT_NEWLINE:
            res.register(self.advance())
        
        if self.current_tok.type == TT_EOF:
            return
        
        ex = res.register(self.expr())
        if res.error: return res

        right = StatementNode(ex, self.rec_stat())
        
        
        return right 
        

    
    
    def expr(self):
        res = ParseResult()
        
        if self.current_tok.matches(TT_KEYWORD, 'VAR'):
            res.register(self.advance())
            
            if self.current_tok.type != TT_INDENTIFIER:
                #print ("EXPECTED IDENT!!!!!")
                return res.failure(ExpectedIdentError('var name'))
            
            var_name = self.current_tok
            res.register(self.advance())
            
            if self.current_tok.type != TT_EQ:
               # print( "EXPECTED =")
                return res.failure(ExpectedSymbolError('='))
    
            res.register(self.advance())
            expr = res.register(self.expr())
            if res.error: return res
            return res.success ( VarAssignNode(var_name, expr))

        
        
        if self.current_tok.matches(TT_KEYWORD, 'extract'):
            res.register(self.advance())
            
            return_ = res.register(self.data_extraction()) 
            if res.error: return res
            return res.success(return_)
        

        if self.current_tok.matches(TT_KEYWORD, 'compute'):
            self.advance()
            if self.current_tok.type == TT_INT:
                expr = res.register(self.computation_percent())
                if res.error: return res
                return res.success(expr)
            expr = res.register(self.computation())
            if res.error: return res
            return res.success(expr)  


        if self.current_tok.matches(TT_KEYWORD, 'show'):
            self.advance() 
            if self.current_tok.type != TT_INDENTIFIER:
                return res.failure(ExpectedIdentError('show var')) 
            show_var = self.current_tok  

            self.advance()

            return ShowNode(show_var)






        # PLOTTING 

        if ( self.current_tok.matches(TT_KEYWORD, 'barplot') or  
         self.current_tok.matches(TT_KEYWORD, 'lmplot') or  
          self.current_tok.matches(TT_KEYWORD, 'scatterplot') or 
           self.current_tok.matches(TT_KEYWORD, 'displot') or 
            self.current_tok.matches(TT_KEYWORD, 'countplot')  ):

            plot_type = self.current_tok
            self.advance()

            if self.current_tok.type != TT_INDENTIFIER:
                return res.failure(ExpectedIdentError('dataframe for plot')) 

            df_name = self.current_tok
            self.advance() 

        

            if  self.current_tok.type != TT_COMMA:
                return res.failure(ExpectedSymbolError(','))
            self.advance() 

            
            if self.current_tok.type != TT_INDENTIFIER:
                return res.failure(ExpectedIdentError('col for plot'))

            x_column = self.current_tok   

            self.advance() 

            if (( self.current_tok.type == TT_COMMA and plot_type.value == 'displot') or 
                ( self.current_tok.type == TT_COMMA and plot_type.value == 'countplot')):
                return res.failure(InvalidSynthaxError('Cant use displot/countplot for y axis'))   

            if  plot_type.value == 'displot' or  plot_type.value == 'countplot':
                return PlotNode(plot_type,df_name,  x_column)

            self.advance() 

            y_column = self.current_tok 

            self.advance()

            if self.current_tok.type != TT_NEWLINE:
                return res.failure(InvalidSynthaxError('invalid chars after 2nd col')) 

            return res.success(PlotNode(plot_type, df_name, x_column, y_column))





        #return None
        if self.current_tok.type != TT_EOF:
            return res.failure(ExpectedIdentError('Smthing wrong'))
    
                
    
    def computation_percent(self):
        res = ParseResult()
        perc_node = self.current_tok
        res.register(self.advance())
        if self.current_tok.type != TT_PERCENT:
            return res.failure(ExpectedSymbolError('%'))
            print('ERRORRR Percent!')
        perc_node = PercentNode(perc_node)
        res.register(self.advance())

        df_node = res.register(self.df_node_parse())
        if res.error: return res

        return res.success(ComputeNode(df_node,perc_node)) 
     
        
    
    
    def computation(self):
        res = ParseResult()
        if  not (self.current_tok.matches(TT_KEYWORD, 'mean') or 
            self.current_tok.matches(TT_KEYWORD, 'stdev') or 
              self.current_tok.matches(TT_KEYWORD, 'max') or 
            self.current_tok.matches(TT_KEYWORD, 'min') or 
            self.current_tok.matches(TT_KEYWORD, 'median') or 
            self.current_tok.matches(TT_KEYWORD, 'sum') ):
            return res.failure(ExpectedIdentError('computational method'))
            
        computation_method = self.current_tok

        res.register(self.advance())

        if not self.current_tok.matches(TT_KEYWORD, 'on'):
            return res.failure(ExpectedIdentError('on'))
            print('ERORR')

        res.register(self.advance())

        if self.current_tok.type != TT_INDENTIFIER:
            return res.failure(ExpectedIdentError('dataframe'))
            print ("EXPECTED Dataset!!!!!!")


        df_node =  res.register(self.df_node_parse())
        if res.error: return res


        return res.success(ComputeNode(df_node, computation_method))
            
                
    
    def df_node_parse(self):
        res = ParseResult()
        df_name = self.current_tok
        res.register(self.advance()) 
        
        cols, rows = res.register(self.check_arr_details())
        if res.error: return res
        
        return res.success(DataframeAccessNode(df_name, cols, rows))
        
        
        
    
    def check_arr_details(self):
        res = ParseResult()
        if self.current_tok.type != TT_LBRACKET:
            return None, None
        
        col_node = res.register(self.check_cols())
        if res.error: return res
        lbracket_bool = False
        if col_node:
            lbracket_bool = True
        row_node = res.register(self.check_rows(lbracket_bool)) 
        if res.error: return res
        
        
        return col_node, row_node
    
    
    
    
    def data_extraction(self):
        res = ParseResult()
        
        if self.current_tok.type != TT_LBRACKET:
            return res.failure(ExpectedSymbolError('['))
            #print('erorrr [')    
        res.register(self.advance())
        left = self.current_tok 
        right = res.register(self.build_column_nodes()) 
        if res.error: return res
        
        if self.current_tok.type != TT_RBRACKET:
            return res.failure(ExpectedSymbolError(']'))
            #print('Error, ]')
        res.register(self.advance()) 
        
        if not self.current_tok.matches(TT_KEYWORD, 'from'):
            return res.failure(ExpectedIdentError('from'))
            #print('Missing from')
        res.register(self.advance())
        
        if self.current_tok.type != TT_PHOTO:
            return res.failure(InvalidSynthaxError('photo expected'))
            #print('erorr on photo')
        source_img = self.current_tok 
        res.register(self.advance())
    

        return res.success(ExtractionNode ( ColumnNode(left,right) , source_img ))

        
        
        
    
    
    def build_column_nodes(self):
        res = ParseResult()
        res.register(self.advance()) 

        if self.current_tok.type == TT_COMMA:
            res.register(self.advance())
            if self.current_tok.type != TT_INDENTIFIER:
                return res.failure((ExpectedIdentError('col name')))
                #print("expected IDENT")
            right = ColumnNode(self.current_tok, res.register(self.build_column_nodes())) 
            if res.error: return res
            return res.success(right)
        return None

        
        
    
    def check_cols(self):
        res = ParseResult()
        self.advance()
        if self.current_tok.type != TT_INDENTIFIER:
            return None    
        
        left = self.current_tok 
        right = res.register(self.build_column_nodes())
        if res.error: return res
        
        if self.current_tok.type != TT_RBRACKET:
            return res.failure(ExpectedSymbolError(']'))
            #print('Error, ]')
        self.advance() 

        return res.success(ColumnNode(left,right))
    
    
    def check_rows(self, bool_):
        res = ParseResult()
        if bool_:
            if self.current_tok.type != TT_LBRACKET:
                return None
            res.register(self.advance())  
        
        det_bool = None
        if self.current_tok.matches(TT_KEYWORD, 'each'):
            det_bool = True
            self.advance()
        
        if self.current_tok.type != TT_INT:
            return res.failure(ExpectedIdentError('row index int'))
            #print('where int')
        nr1 = self.current_tok 
        self.advance()
        
        nr2 = None
        if self.current_tok.matches(TT_KEYWORD, 'to'):
            self.advance() 
            if self.current_tok.type != TT_INT:
                return res.failure(ExpectedIdentError(' to an int'))
            nr2 = self.current_tok
            self.advance()
        
        if self.current_tok.type != TT_RBRACKET:
            return res.failure(ExpectedSymbolError(']'))
            #print('close ]')
        self.advance()

        return res.success(RowNode( nr1, nr2, det_bool))   




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