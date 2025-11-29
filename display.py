from parser import Rule, Or, Sequence, Repeat, Optional, Group, Terminal, NonTerminal
from colors import Color

def gen_proc_for_rule(rule:Rule):
    #Génère la représentation procédurale d'une règle donnée
    lines = []
    name = rule.name
    lines.append(f"{Color.Yellow}function {name}(){Color.Reset} {{")
    body = gen_proc_for_node(rule.definition, ident=1)
    lines.extend(body)
    lines.append("}")
    return "\n".join(lines)

def gen_proc_for_node(node, ident=0):
    #Génère la représentation procédurale d'un noeud donné
    ind = "    " * ident
    lines = []
    
    if isinstance(node, Terminal): #Unité terminale
        lines.append(f"{ind}lire_unite('{node.value}');")
        
    elif isinstance(node, NonTerminal): #Unité non terminale
        lines.append(f"{ind}{Color.Yellow}{node.name}(){Color.Reset};")
        
    elif isinstance(node, Sequence):
        for elem in node.elements:
            lines.extend(gen_proc_for_node(elem, ident))
            
    elif isinstance(node, Or): #Noeud Or(|)
        lines.append(f"{ind}switch (current_token) {{")
        for option in node.options:
            lines.append(f"{ind}    case '{option.value}':")
            body = gen_proc_for_node(option, ident + 2)
            lines.extend(body)
            lines.append(f"{ind}        break;")
        lines.append(f"{ind}}}")
        
    elif isinstance(node, Repeat): #Noeud Repeat({...})
        lines.append(f"{ind}while (true) {{")
        body = gen_proc_for_node(node.content, ident + 1)
        lines.extend(body)
        lines.append(f"{ind}}}")
        
    elif isinstance(node, Optional): #Noeud Optional([...])
        lines.append(f"{ind}if (condition) {{")
        body = gen_proc_for_node(node.content, ident + 1)
        lines.extend(body)
        lines.append(f"{ind}}}")
        
    elif isinstance(node, Group):
        body = gen_proc_for_node(node.content, ident)
        lines.extend(body)
        
    return lines

