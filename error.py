class Error:
    def __init__(self, errorName, details):
        self.errorName = errorName
        self.details = details
    
    def as_string(self):
        return f'{self.errorName} : {self.details}'
    
class IllegalParenthesization(Error):
    def __init__(self,details):
        super().__init__('Improper Parenthesization', details)