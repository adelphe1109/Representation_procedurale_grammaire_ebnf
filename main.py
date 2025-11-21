import lexer

while(True):
    text = input('basic>')
    result = lexer.lexer(text)
    print(result)