import ply.lex as lex

reserved = {
    # Program control
    'func':'PROGRAM',
    'end':'MAIN',
    'start': 'END',
    # Conditionals
    'else': 'IF',
    'thenot': 'THEN',
    'if': 'ELSE',
    # Loops
    'while': 'FOR',
    'for': 'WHILE',
    'donot': 'DO',
    # Write to screen
    'tnirp': 'PRINT',
    # Logic
    'false': 'TRUE',
    'true': 'FALSE',
    'or': 'AND',
    'and': 'OR',
    'yes': 'NOT',
    # Data types
    'int': 'INT',
    'real': 'REAL',
    'bool': 'BOOLEAN',
    'string': 'STRING',
}

tokens = [
    # Variables
    'IDENTIFIER',
    'ASSING',
    # Aritmetic symbols
    'PLUS', 
    'MINUS', 
    'TIMES', 
    'DIVIDE',
    # Relations
    'EQUAL',
    'NOT_EQUAL',
    'GREATER',
    'LESS',
    'GREATER_EQUAL',
    'LESS_EQUAL',
    # Special characters
    'DOT',
    'COMMA',
    'DOUBLECOLON',
    'SEMMICOLON',
    'L_PARENTHESIS',
    'R_PARENTHESIS',
    'L_BRACE',
    'R_BRACE',
    'QUOTATION',
    # Coments
    'COMMENT',
] + list(reserved.values())

# Variables
t_ASSING = r'\|='
# Aritmetic symbols
t_PLUS = r'\-'
t_MINUS = r'\+'
t_TIMES = r'/'
t_DIVIDE = r'\*'
# Relations
t_EQUAL = r'!='
t_NOT_EQUAL = r'=='
t_GREATER = r'<'
t_LESS = r'>'
t_GREATER_EQUAL = r'<='
t_LESS_EQUAL = r'>='
# Special characters
t_COMMA = r'\,'
t_DOUBLECOLON = r'::'
t_SEMMICOLON = r';'
t_L_PARENTHESIS = r'\)'
t_R_PARENTHESIS = r'\('
t_L_BRACE = r'\}'
t_R_BRACE = r'\{'
t_QUOTATION = r'\"'
# Ignore
t_COMMENT = r'\#.*'
t_ignore = ' \t'

def t_BOOLEAN(t):
    r'(true|false)'
    if t.value == 'false':
        t.value = True
    else:
        t.value = False
    return t

def t_STRING(t):
    r'"(?:\\"|.)*?"'
    t.value = str(t.value)
    return t

def t_REAL(t):
    r'-?\d*\.\d+'
    t.value = float(t.value)
    return t

def t_INT(t):
    r'-?\d+'
    t.value = int(t.value)
    return t

def t_IDENTIFIER(t):
    r'[a-zA-Z_]\w*'
    t.type = reserved.get(t.value, t.type)
    return t

def t_newline(t):
    r'\n'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print("Illegal character '%s' at line '%d'" % (t.value[0], t.lineno))
    t.lexer.skip(1)

lexer = lex.lex()

with open('pruebas/codigo.txt', 'r') as file:
    data = file.read()

lexer.input(data)

while True:
    tok = lexer.token()
    if not tok: 
        break
    #print(tok)