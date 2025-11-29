from lexer import Token

class Node : pass

class Grammar(Node):
    def __init__(self, rules):
        self.rules = rules
    def __repr__(self):
        return f"Grammar({self.rules})"

class Rule(Node):
    def __init__(self, name, definition):
        self.name = name
        self.definition = definition
    def __repr__(self):
        return f"Rule({self.name} , {self.definition})"

class Or(Node):
    def __init__(self, options):
        self.options = options
    def __repr__(self):
        return f"Or({self.options})"

class Sequence(Node):
    def __init__(self, elements):
        self.elements = elements
    def __repr__(self):
        return f"Sequence({self.elements})"

class Repeat(Node):
    def __init__(self, content):
        self.content = content
    def __repr__(self):
        return f"Repeat({self.content})"

class Optional(Node):
    def __init__(self, content):
        self.content = content
    def __repr__(self):
        return f"Optional({self.content})"

class Group(Node):
    def __init__(self, content):
        self.content = content
    def __repr__(self):
        return f"Group({self.content})"

class Terminal(Node):
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"Terminal('{self.value}')"

class NonTerminal(Node):
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return f"NonTerminal({self.name})"

class Parser:
    """Implémente un analyseur syntaxique pour une grammaire EBNF."""
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[self.pos] if self.tokens else Token("EOF", "")

    def advance(self):
        """Passe au jeton suivant."""
        self.pos += 1
        self.current_token = self.tokens[self.pos] if self.pos < len(self.tokens) else Token("EOF", "")
        return self.current_token

    def check(self, token_type):
        """Vérifie si le jeton actuel est du type attendu, sans avancer."""
        return self.current_token.type == token_type

    def consume(self, token_type):
        """Consomme (vérifie et avance) le jeton actuel."""
        if self.check(token_type):
            token = self.current_token
            self.advance()
            return token
        
        raise SyntaxError(
            f"Erreur de syntaxe: Attendu '{token_type}', "
            f"trouvé '{self.current_token.type}' ('{self.current_token.value}') "
            f"à la position de jeton {self.pos}"
        )

    
    def parse_Grammar(self):
        """Analyse une suite de règles EBNF et retourne une liste (l'AST)."""
        grammar_rules = []
        while not self.check("EOF"):
            grammar_rules.append(self.parse_Rule())
        return Grammar(grammar_rules)

   
    def parse_Rule(self):
        """Analyse une seule règle : ID = ... ;"""
        name = self.consume("ID").value
        self.consume("ASSIGN")
        
        # Le corps de la règle est une Expression_EBNF
        definition = self.parse_Expression_EBNF()
        
        self.consume("SEMI")
        
        return Rule(name, definition)

   
    def parse_Expression_EBNF(self):
        """Gère les alternatives (|) dans le corps d'une règle."""
        sequence = self.parse_Sequence()
        
        alternatives = [sequence]
        while self.check("OR"):
            self.consume("OR")
            alternatives.append(self.parse_Sequence())
            
        
        if len(alternatives) > 1:
            return Or(alternatives)
        else:
            return sequence


    def parse_Sequence(self):
        """Gère la séquence d'éléments (A B C) : concaténation implicite."""
        elements = [self.parse_Element_EBNF()] # Un élément est toujours attendu
        
        
        TERMINATORS = ("OR", "SEMI", "RPAREN", "RBRACK", "RBRACE", "EOF")

        
        while self.current_token.type not in TERMINATORS:
            
            
            if self.check("COMMA"):
                self.consume("COMMA")
            
           
            if self.current_token.type in TERMINATORS:
                break 

            
            elements.append(self.parse_Element_EBNF())
            
       
        if len(elements) > 1:
            return Sequence(elements)
        else:
            return elements[0]


    
    def parse_Element_EBNF(self):
        """Identifie et analyse les constructions EBNF de base."""
        
       
        if self.check("LBRACE"):
            self.consume("LBRACE")
            content = self.parse_Expression_EBNF()
            self.consume("RBRACE")
            return Repeat(content)

        
        elif self.check("LBRACK"):
            self.consume("LBRACK")
            content = self.parse_Expression_EBNF()
            self.consume("RBRACK")
            return Optional(content)

       
        elif self.check("LPAREN"):
            self.consume("LPAREN")
            content = self.parse_Expression_EBNF()
            self.consume("RPAREN")
            return Group(content)
        
        
        elif self.check("TERMINAL"):
            return Terminal(self.consume("TERMINAL").value)

        
        elif self.check("ID"):
            return NonTerminal(self.consume("ID").value)
            
        
        else:
            raise SyntaxError(
                f"Erreur EBNF: Attendu un ID, TERMINAL, '(', '[', ou '{{', "
                f"trouvé {self.current_token.type} ('{self.current_token.value}')"
            )