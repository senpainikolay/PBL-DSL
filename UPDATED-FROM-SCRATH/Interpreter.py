from Parser import ParseResult 
from Parser import EachNode



import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns

class DF:
    def __init__(self, dataframe):
        self.dataframe  = dataframe 
    
    def selected_cols(self, col_arr):
        return DF(self.dataframe[col_arr])
    
    def select_1idx_row(self, idx):
        return DF(self.dataframe.iloc[idx,:])
    
    def select_2idx_row(self, idx1,idx2):
        return DF(self.dataframe.iloc[idx1:idx2,:])
    
    def select_each_row(self,idx):
        return DF(self.dataframe.groupby(np.arange(len(self.dataframe)) // idx ))
    
    def __repr__(self):
        return f'{self.dataframe}'
        
        
        
    
class SymbolTable:
    def __init__(self):
        self.symbols = {}
    def get(self, name):
        res = ParseResult()
        value = self.symbols.get(name)
        #if value.bool():
            #pass
        return value
        #return res.failure('FAILBRAT')
    
    def set(self,name,value):
        self.symbols[name] = value
    def remove(self, name):
        del self.symbols[name] 


from app import main_run 


class Interpreter:
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.res = ParseResult()
        
    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node)
    def no_visit_method(self,node):
        raise Exception(f'No visit_{type(node).__name__} method defined') 
        
        
    def visit_StatementNode(self,node):
        self.res.register(self.visit(node.val))
        if  self.res.error: return self.res, None
        return self.res, node.right
        
    
    def visit_VarAssignNode(self,node):
        df_name = self.res.register(self.visit(node.var_name_tok))
        if self.res.error: return self.res
        assigned_df = self.res.register(self.visit(node.value_node))
        if self.res.error: return self.res
        self.symbol_table.set(df_name, assigned_df)
        #print(self.symbol_table.symbols)

        #print('found var assignnode')   
        
    def visit_ComputeNode(self,node):
        
        df = self.res.register(self.visit(node.dataframe))
        if self.res.error: return self.res


        measure  = self.visit(node.method) 


        if str(measure).isnumeric():
            df = ( df * measure ) / 100 

        #print(measure)
        

        if measure == "mean":
            df = df.mean()
        elif measure == "stdev":
            df = df.std()
        elif measure == "max":
            df = df.max()
        elif measure == "min":
            df = df.min()
        elif measure == "median":
            df = df.median()
        elif measure == "sum":
            df = df.sum()

        return df

        
    def visit_Token(self,node):
        return node.value
        #print('found Token Node')   


    def visit_ShowNode(self,node):


        name = self.visit(node.val)  
        val = self.res.register(self.symbol_table.get(name))
        if self.res.error: return self.res
        print(f'--------- PRINTING dataframe name:  {name}-----------')
        print(val)



    def visit_PlotNode(self,node):
        plot_type = self.visit(node.type)
        df = self.visit(node.df)
        X = self.visit(node.x)
        if node.y:
            Y = self.visit(node.y)

        df = self.res.register(self.symbol_table.get(df))
        if self.res.error: return self.res   


        if plot_type == "lmplot" or plot_type == "scatterplot" or plot_type == "barplot":
            
            if plot_type == "lmplot":
                # encoding categorial values
                replace_map = {}
                df1 = df.copy()
                
                for i in df.columns:
                    if df[i].dtypes == 'O':
                        labels = df[i].astype('category').cat.categories.tolist()
                        replace_map = {i: {k: v for k, v in zip(labels, list(range(0, len(labels))))}}
                df1.replace(replace_map, inplace=True)

                # printing the replaced values for lmplot since it doesn't work on string values
                print("LMPLOT REPLACED VALUES:")
                print(replace_map)
                print()

                # showing the plot
                sns.lmplot(x=X, y=Y, data=df1)
                plt.show()
                
            elif plot_type == "scatterplot":
                # showing the plot
                sns.scatterplot(x=X, y=Y, data=df)
                plt.show()
                
            elif plot_type == "barplot":
                # showing the plot
                sns.barplot(x=X, y=Y, data=df)
                plt.show() 


        # plots for which 1 column - x needs to be specified
        if plot_type == "displot" or plot_type == "countplot":
            
            if plot_type == "displot":
                sns.displot(x=X, data=df)
                plt.show()
            elif plot_type == "countplot":
                sns.countplot(x=X, data=df)
                plt.show()


        
    def visit_DataframeAccessNode(self,node):
        df = self.visit(node.name) 
        df = self.res.register(self.symbol_table.get(df))
        if self.res.error: return self.res 
        if node.colNode:
            cols_arr = []
            val, next_node =self.visit(node.colNode)
            cols_arr.append(val)
            while next_node:
                val, next_node = self.visit(next_node)
                cols_arr.append(val)
            df = df[cols_arr] 
        if node.rowNode:
            a,b,c = self.visit(node.rowNode)
            if a:
                df = DF(df).select_each_row(a).dataframe
                
            if b and not c:
                df = DF(df).select_1idx_row(b).dataframe
                
            if b and c:
            
                df = DF(df).select_2idx_row(b,c).dataframe 
            
        return df


            
        

        #print(self.res.error)
    
    
    def visit_ColumnNode(self,node):
        return self.visit(node.val), node.right

    
    def visit_ExtractionNode(self,node):
        img_src = self.visit(node.source)
        col_name, next_node =self.visit(node.cols)
        
        df = main_run(img_src, col_name)
        while next_node:
            col_name, next_node = self.visit(next_node)
            df2 = main_run(img_src,col_name)
            df = pd.concat( [df,df2],axis = 1)
 
        return df

        
    def visit_MethodNode(self,node):
        return self.visit(node.method) 
        
    def visit_RowNode(self,node):
        if type(node.nr1) == EachNode:
            return  self.visit(node.nr1), None, None
        nr1 = self.visit(node.nr1)
        nr2 = None
        if node.nr2:
            nr2 = self.visit(node.nr2)
        return None, nr1, nr2
        
    def visit_ToNode(self,node):
        return self.visit(node.val)
        
          
    def visit_EachNode(self,node):
        return self.visit(node.val)
        
          
    def visit_PercentNode(self,node):
        return self.visit(node.nr)