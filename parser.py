from lexer import Token 

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
        return ("GRAMMAR", grammar_rules)

   
    def parse_Rule(self):
        """Analyse une seule règle : ID = ... ;"""
        rule_id = self.consume("ID").value
        self.consume("ASSIGN")
        
        # Le corps de la règle est une Expression_EBNF
        definition = self.parse_Expression_EBNF()
        
        self.consume("SEMI")
        
        return ("RULE", rule_id, definition)

   
    def parse_Expression_EBNF(self):
        """Gère les alternatives (|) dans le corps d'une règle."""
        sequence = self.parse_Sequence()
        
        alternatives = [sequence]
        while self.check("OR"):
            self.consume("OR")
            alternatives.append(self.parse_Sequence())
            
        
        if len(alternatives) > 1:
            return ("ALTERNATIVES", alternatives)
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
            return ("SEQUENCE", elements)
        else:
            return elements[0]


    
    def parse_Element_EBNF(self):
        """Identifie et analyse les constructions EBNF de base."""
        
       
        if self.check("LBRACE"):
            self.consume("LBRACE")
            content = self.parse_Expression_EBNF()
            self.consume("RBRACE")
            return ("REPETITION", content)

        
        elif self.check("LBRACK"):
            self.consume("LBRACK")
            content = self.parse_Expression_EBNF()
            self.consume("RBRACK")
            return ("OPTIONNEL", content)

       
        elif self.check("LPAREN"):
            self.consume("LPAREN")
            content = self.parse_Expression_EBNF()
            self.consume("RPAREN")
            return ("GROUP", content)
        
        
        elif self.check("TERMINAL"):
            return ("TERMINAL", self.consume("TERMINAL").value)

        
        elif self.check("ID"):
            return ("NON_TERMINAL", self.consume("ID").value)
            
        
        else:
            raise SyntaxError(
                f"Erreur EBNF: Attendu un ID, TERMINAL, '(', '[', ou '{{', "
                f"trouvé {self.current_token.type} ('{self.current_token.value}')"
            )