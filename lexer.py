import re
import error

TOKENS = [
    
    ("SKIP", r"[ \t\r\n]+"),
    ("TERMINAL", r"\"[^\"]*\"|'[^']*'"),
    ("ASSIGN", r"="),     
    ("OR", r"\|"),        
    ("SEMI", r";"),
    ("LBRACK", r"\["),    
    ("RBRACK", r"\]"),    
    ("LBRACE", r"\{"),    
    ("RBRACE", r"\}"),    
    ("LPAREN", r"\("),    
    ("RPAREN", r"\)"),    
    ("COMMA", r","),
    ("GT", r">"),
    ("LT", r"<"),
    ("PLUS", r"\+"),
    ("MINUS", r"-"),
    ("MUL", r"\*"),
    ("DIV", r"/"),
    ("ID", r"[A-Za-z_][A-Za-z0-9_]*"),
    ("OTHER", r"."),
]

master_re = re.compile("|".join("(?P<%s>%s)" % pair for pair in TOKENS), re.S)

class Token : 
    def __init__(self, type_, value):
        self.type = type_
        self.value = value
    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)})"
    
def well_parenthesized(text):
    stack = []
    pairs = {')': '(', ']': '[', '}': '{'}

    for char in text:
        if char in "([{":
            stack.append(char)
        elif char in ")]}":
            if not stack or stack[-1] != pairs[char]:
                return False
            stack.pop()

    return len(stack) == 0


def lexer(text):
    tokens = []
    if well_parenthesized(text) :
        for m in master_re.finditer(text):
            typ = m.lastgroup
            val = m.group(0)
            
            if typ == "SKIP":
                continue
            
            
            if typ == "TERMINAL":
                if (val.startswith('"') and val.endswith('"')) or \
                (val.startswith("'") and val.endswith("'")):
                    val = val[1:-1]
                
            tokens.append(Token(typ, val))
        tokens.append(Token("EOF", ""))
        return tokens, None
    else :
        return [], error.IllegalParenthesization(text)