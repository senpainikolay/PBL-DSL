
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