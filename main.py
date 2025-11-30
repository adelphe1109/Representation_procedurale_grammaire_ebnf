from lexer import lexer, Token
from parser import Parser, Grammar 
from display import gen_proc_for_rule
from colors import Color

def run_parser_test(code):
    """Exécute l'analyse lexicale, syntaxique et la génération de code pour une règle donnée."""
    print(f"\n--- Analyse de : '{code}' ---")
    
    
    tokens, error = lexer(code)
    
    if error:
        print(f"{Color.Red}Erreur Lexicale : {error.as_string()}{Color.Reset}")
        return 
    else:
        print(f"{Color.Green}Tokens : {tokens}{Color.Reset}")
    
    
    
    try:
        parser = Parser(tokens)
        
        ast_object = parser.parse_Grammar() 

        
        print(f"{Color.Blue}Analyse Réussie (AST) : {ast_object}{Color.Reset}")

        
        if not parser.check("EOF"):
            print(f"{Color.Yellow}[ATTENTION] Jetons non consommés : {parser.current_token}{Color.Reset}")
    
        
        if isinstance(ast_object, Grammar) and ast_object.rules:
            
            first_rule = ast_object.rules[0]
            lines = gen_proc_for_rule(first_rule)
            print("\nCode Procédural Généré :\n", lines)
        else:
             print(f"{Color.Yellow}Attention: L'AST est vide ou incomplet. Aucune règle à générer.{Color.Reset}")

    except Exception as e:
        print(f"{Color.Red}Erreur de compilation (Syntaxique ou Interne) : {e}{Color.Reset}")



if __name__ == "__main__":
    
    
    print("Test Critique : Règle complète avec terminaux.")
    run_parser_test('Expression = SExpr[("="|">"|"<")SExpr];')
    run_parser_test('SExpr = ["+"|"-"]Term { ("+"|"-") Term } ;')
    
    
    run_parser_test('Liste = ID { "," ID } ;')
    run_parser_test('Bloc = "(" (A | B) ;') 
    
    print("\n--- Mode Interactif ---")
    while(True):
        try:
            text = input('basic>')
            if text.lower() == 'exit':
                break
            
            
            tokens, error = lexer(text)
            if error:
                print(f"{Color.Red}Erreur Lexicale : {error.as_string()}{Color.Reset}")
                continue
            
            print(f"{Color.Green}Tokens : {tokens}{Color.Reset}")
            
            
            parser = Parser(tokens)
            ast_object = parser.parse_Grammar()
            print(f"{Color.Blue}AST : {ast_object}{Color.Reset}")

            
            if isinstance(ast_object, Grammar) and ast_object.rules:
                first_rule = ast_object.rules[0]
                lines = gen_proc_for_rule(first_rule)
                print("\nReprésentation procédurale:\n", lines)
            else:
                 print(f"{Color.Yellow}Attention: L'AST est vide ou incomplet. Aucune règle à générer.{Color.Reset}")
            
        except EOFError:
            break
        except Exception as e:
            
            print(f"{Color.Red}Erreur d'exécution: {type(e).__name__}: {e}{Color.Reset}")