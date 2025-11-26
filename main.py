from lexer import lexer, Token
from parser import Parser 
import sys

def run_parser_test(code):
    """Exécute l'analyse lexicale et syntaxique pour un code donné."""
    print(f"\n--- Analyse de : '{code}' ---")
    
    
    tokens, error = lexer(code)
    if error:
        print(f"Erreur Lexicale : {error.as_string()}")
    else:
        print("Tokens :", tokens)
    
   
        try:
            parser = Parser(tokens)
            
            ast = parser.parse_Grammar()
            
            print("Analyse Réussie (AST) :", ast)
            
            if not parser.check("EOF"):
                print(f"[ATTENTION] Jetons non consommés : {parser.current_token}")
                
        except Exception as e:
            print(f"Erreur de compilation : {e}")



if __name__ == "__main__":
    
    
    print("Test Critique : Règle complète avec terminaux.")
    run_parser_test('Expression = SExpr[("="|">"|"<")SExpr];')
    
    
    run_parser_test('Liste = ID { "," ID } ;')
    run_parser_test('Bloc = "(" (A | B) ";" ;')


    
    print("\n--- Mode Interactif ---")
    while(True):
        try:
            text = input('basic>')
            if text.lower() == 'exit':
                break
            
            tokens = lexer(text)
            print("Tokens:", tokens)
            
            parser = Parser(tokens)
            ast = parser.parse_Grammar()
            print("AST:", ast)
            
        except EOFError:
            break
        except Exception as e:
            print(f"Erreur: {e}")