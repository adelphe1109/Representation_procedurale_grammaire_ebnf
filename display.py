from parser import Rule, Or, Sequence, Repeat, Optional, Group, Terminal, NonTerminal
from colors import Color
import sys 

INDENT_UNIT = "    " 

def get_first_tokens(node):
    
    if isinstance(node, Terminal):
        return [node.value]
    if isinstance(node, NonTerminal):
        return []
    if isinstance(node, Group) or isinstance(node, Optional) or isinstance(node, Repeat):
        return get_first_tokens(node.content)
    if isinstance(node, Sequence):
        return get_first_tokens(node.elements[0])
    if isinstance(node, Or):
        tokens = []
        for option in node.options:
            tokens.extend(get_first_tokens(option))
        return list(set(tokens)) 
    return []


def gen_proc_for_rule(rule: Rule):
    lines = []
    name = rule.name
    lines.append(f"{Color.Yellow}def parse_{name}(self):{Color.Reset}")
    body = gen_proc_for_node(rule.definition, ident=1)
    lines.extend(body)
    lines.append(f"{INDENT_UNIT}return None") 
    return "\n".join(lines)


def gen_proc_for_node(node, ident=0):
    ind = INDENT_UNIT * ident
    lines = []
    
    # ------------------ Terminaux et NonTerminaux ------------------
    if isinstance(node, Terminal):
        lines.append(f"{ind}self.consume('TERMINAL') # Attendu : '{node.value}'")
        
    elif isinstance(node, NonTerminal):
        lines.append(f"{ind}{Color.Yellow}self.parse_{node.name}(){Color.Reset}")


    # ------------------ Structures de Contrôle ------------------
    elif isinstance(node, Sequence):
        for elem in node.elements:
            lines.extend(gen_proc_for_node(elem, ident))
            
    elif isinstance(node, Group):
        lines.extend(gen_proc_for_node(node.content, ident))
            
    elif isinstance(node, Optional): 
        first_tokens = get_first_tokens(node.content)
        tokens_str = ", ".join(f"'{t}'" for t in first_tokens)
        
        lines.append(f"{ind}# Début OPTIONAL (First Set: {tokens_str})")
        lines.append(f"{ind}if self.current_token.value in ({tokens_str}):")
        
        body = gen_proc_for_node(node.content, ident + 1)
        lines.extend(body)
        
    elif isinstance(node, Or): 
        lines.append(f"{ind}# Début ALTERNATIVE (|)")
        

        for i, option in enumerate(node.options):
            first_tokens = get_first_tokens(option)
            tokens_str = ", ".join(f"'{t}'" for t in first_tokens)
            

            keyword = "if" if i == 0 else "elif"
            
            lines.append(f"{ind}{keyword} self.current_token.value in ({tokens_str}):")
            body = gen_proc_for_node(option, ident + 1)
            lines.extend(body)
            

        lines.append(f"{ind}else:")
        lines.append(f"{ind}{INDENT_UNIT}raise SyntaxError('Alternative in OR not matched.')")
        
    elif isinstance(node, Repeat):
        first_tokens = get_first_tokens(node.content)
        tokens_str = ", ".join(f"'{t}'" for t in first_tokens)
        
        lines.append(f"{ind}# Début REPEAT (First Set: {tokens_str})")
        

        lines.append(f"{ind}while self.current_token.value in ({tokens_str}):")
        
        body = gen_proc_for_node(node.content, ident + 1)
        lines.extend(body)
            
    return lines