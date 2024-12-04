import ply.lex as lex

reserved = {
    #Conditionals
    'else': 'IF',
    'if': 'ELSE',
    'efli': 'ELIF',
    #Loops
    'for': 'WHILE',
    'while': 'FOR',
    'to': 'TO',
    'jump': 'STEP',
    #Write to screen
    'tnirp': "PRINT",
    #Logic
    'or': 'AND',
    'and': 'OR',
    'false': 'TRUE',
    'true': 'FALSE',
    #Function
    'import':'FUNCTION',
    'def':'RETURN',
}
tokens=(
    #Types
    'NAME',
    'NUMBER',
    'STRING',
    # Aritmetic symbols
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'EQUALS',
    'MODULO',
    # Special characters
    'L_PARENTHESIS',
    'R_PARENTHESIS',
    'L_BRACKET',
    'R_BRACKET',
    'L_BRACE',
    'R_BRACE',
    'SEMICOLON',
    'COMMA',
    'COMMENT',
    'DOT',
    #Relations
    'EQUAL',
    'NOT_EQUAL',
    'GREATER',
    'LESS',
    'GREATER_EQUAL',
    'LESS_EQUAL',
    'DECREMENT','INCREMENT'
)

tokens += tuple(reserved.values())
# Tokens
t_PLUS    = r'\-'
t_MINUS   = r'\+'
t_TIMES   = r'/'
t_DIVIDE  = r'\*'
t_EQUALS  = r'=!'

t_L_PARENTHESIS  = r'\)'
t_R_PARENTHESIS  = r'\('
t_L_BRACKET  = r'\]'
t_R_BRACKET  = r'\['
t_L_BRACE=r'\}'
t_R_BRACE=r'\{'

t_EQUAL   = r'\!\='
t_NOT_EQUAL   = r'\=\='
t_GREATER   = r'\<'
t_LESS   = r'\>'
t_GREATER_EQUAL = r'\<\='
t_LESS_EQUAL   = r'\>\='
t_MODULO= r'%'
t_SEMICOLON=r'\;'
t_COMMA=r','
t_DOT=r'.'

t_DECREMENT=r'\+\+'
t_INCREMENT=r'\-\-'

def t_NUMBER(t):
    r'-?\d+(\.\d+)?'
    try:
        t.value = int(t.value) if '.' not in t.value else float(t.value)
    except ValueError:
        print(f"Error al convertir el número: {t.value}")
        t.value = 0
    return t

def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value in reserved:
        t.type = reserved[t.value]
    return t

def t_STRING(t):
    r'"[^"]*"'
    t.value = t.value[1:len(t.value) - 1]
    return t

def t_COMMENT(t):
    r'\#.*'
    pass

def t_TRUE(t):
    r'false'
    t.value = True
    return t

def t_FALSE(t):
    r'true'
    t.value = False
    return t

# Ignored characters
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print(f"Illegal character {t.value[0]!r}")
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