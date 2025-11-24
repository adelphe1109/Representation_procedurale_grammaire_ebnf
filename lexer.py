import re
import error

TOKENS = [
    ("SKIP", r"[ \t\r\n]+"),             
    ("ID", r"[A-Za-z_][A-Za-z0-9_]*"),
    ("STRING", r"'([^'\\]|\\.)*'|\"([^\"\\]|\\.)*\""),
    ("ASSIGN", r"="),
    ("PLUS", r"\"\+\""),
    ("MINUS", r"\"-\""),
    ("MUL", r"\"\*\""),
    ("DIV", r"\"/\""),
    ("SEMI", r";"),
    ("OR", r"\|"),
    ("LBRACE", r"\{"),
    ("RBRACE", r"\}"),
    ("LBRACK", r"\["),
    ("RBRACK", r"\]"),
    ("LPAREN", r"\("),
    ("RPAREN", r"\)"),
    ("COMMA", r","),
    ("OTHER", r"."),
]

master_re = re.compile("|".join("(?P<%s>%s)" % pair for pair in TOKENS), re.S)

class Token : 
    def __init__(self, type_, value):
        self.type = type_
        self.value = value
    def __repr__(self):
        return f"Token({self.type}, {self.value})"
    
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
    if well_parenthesized(text):
        for m in master_re.finditer(text):
            typ = m.lastgroup
            val = m.group(0)
            if typ == "SKIP" or typ == "COMMENT":
                continue
            if typ == "STRING":
                inner = val[1:-1]
                inner = bytes(inner, "utf-8").decode("unicode_escape")
                single_map = {
                    "+": "PLUS", "-": "MINUS", "*": "MUL", "/": "DIV",
                    "|": "OR", "{": "LBRACE", "}": "RBRACE",
                    "[": "LBRACK", "]": "RBRACK", "(": "LPAREN",
                    ")": "RPAREN", ",": "COMMA", ";": "SEMI", "=": "ASSIGN",
                }
                if len(inner) == 1 and inner in single_map:
                    tokens.append(Token(single_map[inner], inner))
                    continue
                else:
                    tokens.append(Token("STRING", inner))
                    continue
            tokens.append(Token(typ, val))
        tokens.append(Token("EOF", ""))
        return tokens, None
    else:
        return [], error.IllegalParenthesization(text)
        