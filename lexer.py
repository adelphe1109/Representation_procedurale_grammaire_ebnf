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
    opening = {'(': ')', '{': '}', '[': ']'}
    closing = {')': '(', '}': '{', ']': '['}

    stack = []
    in_string = False
    string_char = None  # ' or "

    for ch in text:
        # Gestion des chaînes
        if in_string:
            if ch == string_char:
                in_string = False
            continue

        # Début d'une chaîne
        if ch in ('"', "'"):
            in_string = True
            string_char = ch
            continue

        # Si c'est un bracket ouvrant
        if ch in opening:
            stack.append(ch)
            continue

        # Si c'est un bracket fermant
        if ch in closing:
            if not stack:
                return False
            if stack[-1] != closing[ch]:
                return False
            stack.pop()

    # Expression bien formée si :
    # - pas de string non fermée
    # - pile vide
    return not in_string and not stack


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