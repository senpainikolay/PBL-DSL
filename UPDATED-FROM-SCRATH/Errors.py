
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