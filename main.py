from lexer import lexer, Token
from parser import Parser
from display import gen_proc_for_rule
from colors import Color

def run_parser_test(code):
    """Exécute l'analyse lexicale et syntaxique pour un code donné."""
    print(f"\n--- Analyse de : '{code}' ---")
    
    
    tokens, error = lexer(code)
    if error:
        print(f"{Color.Red}Erreur Lexicale : {error.as_string()}{Color.Reset}")
    else:
        print(f"{Color.Green}Tokens : {tokens}{Color.Reset}")
    
   
        try:
            parser = Parser(tokens)
            
            ast = parser.parse_Grammar()

            
            print(f"{Color.Blue}Analyse Réussie (AST) : {ast}{Color.Reset}")
            
            if not parser.check("EOF"):
                print(f"[ATTENTION] Jetons non consommés : {parser.current_token}")
            
            rules = ast.rules
            lines = gen_proc_for_rule(rules[0])
            print("\nCode Généré :\n", lines)
                
        except Exception as e:
            print(f"Erreur de compilation : {e}")



if __name__ == "__main__":
    
    
    print("Test Critique : Règle complète avec terminaux.")
    run_parser_test('Expression = SExpr[("="|">"|"<")SExpr];')
    run_parser_test('SExpr = ["+"|"-"]Term { ("+"|"-") Term } ;')
    
    
    run_parser_test('Liste = ID { "," ID } ;')
    run_parser_test('Bloc = "(" (A | B) ";" ;')


    
    print("\n--- Mode Interactif ---")
    while(True):
        try:
            text = input('basic>')
            if text.lower() == 'exit':
                break
            
            tokens, error = lexer(text)
            if error:
                print(f"{Color.Red}Erreur Lexicale : {error.as_string()}{Color.Reset}")
            else:
                print(f"{Color.Green}Tokens : {tokens}{Color.Reset}")
            
            parser = Parser(tokens)
            ast = parser.parse_Grammar()
            print(f"{Color.Blue}AST : {ast}{Color.Reset}")

            rules = ast.rules
            lines = gen_proc_for_rule(rules[0])
            print("\nReprésentation procédurale:\n", lines)
            
        except EOFError:
            break
        except Exception as e:
            print(f"Erreur: {e}")