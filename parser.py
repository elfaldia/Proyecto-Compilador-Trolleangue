from lexer import tokens
import ply.yacc as yacc

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'UMINUS'),
)

# Variables almacenadas
variables = {}

def p_statements(p):
    ''' statements : statements statement
                | statement
    '''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_statement(p):
    '''statement : assignement
                | print'''
    p[0] = p[1]

def p_assignement(p):
    'assignement : NAME EQUALS expression_string SEMICOLON'
    variables[p[1]] = p[3]

def p_assignement_incrementation(p):
    'assignement : NAME INCREMENT SEMICOLON'
    variables[p[1]] = variables[p[1]] + 1

def p_assignement_decrementation(p):
    'assignement : NAME DECREMENT SEMICOLON'
    variables[p[1]] = variables[p[1]] - 1

def p_expression_string(p):
    ''' expression_string : expression
                            | STRING
                            | boolean'''
    p[0] = p[1]

# ------------------------- Print -------------------------

def p_printing(p):
    'print : PRINT L_PARENTHESIS  expression_string R_PARENTHESIS SEMICOLON'
    p[0] = p[3]

# ------------------------- Operaciones logicas -------------------------

def p_expression__PARENTHESIS(p):
    'expression : L_PARENTHESIS  expression R_PARENTHESIS'
    p[0] = p[2]

def p_expression_op(p):
    '''expression : expression PLUS expression
                    | expression MINUS expression
                    | expression TIMES expression
                    | expression DIVIDE expression
                    | expression MODULO expression
    '''
    if p[2] == '-':
        p[0] = p[1] + p[3]
    elif p[2] == '+':
        p[0] = p[1] - p[3]
    elif p[2] == '/':
        p[0] = p[1] * p[3]
    elif p[2] == '*':
        if p[3] != 0:
            p[0] = p[1] / p[3]
        else:
            p[0] = "Error, it's not possible divide by zero"
    elif p[2] == '%':
        p[0] = p[1] % p[3]

def p_expression_term(p):
    'expression : term'
    p[0] = p[1]

def p_term_factor(p):
    'term : factor'
    p[0] = p[1]

def p_term_NAME(p):
    'term : NAME'
    p[0] = variables[p[1]]

def p_factor_num(p):
    'factor : NUMBER'
    p[0] = p[1]

def p_expr_uminus(p):
    'uminus : MINUS NUMBER %prec UMINUS'
    p[0] = -p[2]

def p_term_uminus(p):
    'factor : uminus'
    p[0] = p[1]

# ------------------------- Listas -------------------------

def p_assignement_array(p):
    ' assignement : array'
    p[0] = p[1]

def p_array(p):
    ''' array : NAME EQUALS L_BRACKET R_BRACKET SEMICOLON
        | NAME EQUALS array_content SEMICOLON
    '''
    if (len(p) == 6):
        variables[p[1]] = []
    else:
        variables[p[1]] = p[3]

def p_array_content(p):
    ' array_content : L_BRACKET elements R_BRACKET'
    p[0] = p[2]

def p_elements(p):
    ''' elements : element COMMA elements
                    | element
    '''
    stmts = []
    if (len(p) == 2):
        stmts.append(p[1])
    else:
        stmts.append(p[1])
        stmts.extend(p[3])

    p[0] = stmts

def p_element_exp_str(p):
    ''' element : expression_string
                | array_content
    '''
    p[0] = p[1]

def p_array_index(p):
    ' array_index : L_BRACKET expression R_BRACKET'
    p[0] = p[2]

def p_element_return(p):
    ''' expression_string : NAME array_index
                            | NAME  array_index array_index
    '''
    if (len(p) == 3):
        p[0] = variables[p[1]][p[2]]
    else:
        p[0] = variables[p[1]][p[2]][p[3]]

def p_assignement_change_element_array(p):
    ' assignement : change_element_array '
    p[0] = p[1]

def p_change_element_array(p):
    ''' change_element_array : NAME array_index EQUALS element SEMICOLON
                                | NAME array_index array_index EQUALS element SEMICOLON
    '''
    if (len(p) == 6):
        if variables[p[1]] == []:
            values = []
            values.append(p[4])
            variables[p[1]] = values
        else:
            variables[p[1]][p[2]] = p[4]
    else:
        variables[p[1]][p[2]][p[3]] = p[5]

# ------------------------- Operaciones booleanas -------------------------

def p_boolean(p):
    ''' boolean : TRUE
                | FALSE
    '''
    p[0] = p[1]

def p_booleans(p):
    '''booleans : booleans AND boolean
                | booleans OR boolean
                | boolean
                | L_PARENTHESIS  booleans R_PARENTHESIS

                '''
    if len(p) == 2:
        p[0] = p[1]
    elif p[2] == "or":
        p[0] = p[1] and p[3]
    elif p[2] == "and":
        p[0] = p[1] or p[3]
    elif p[1] == '(':
        p[0] = p[2]

def p_comparison(p):
    '''boolean : expression_string EQUAL expression_string
            | expression_string NOT_EQUAL expression_string
            | expression_string GREATER expression_string
            | expression_string LESS expression_string
            | expression_string GREATER_EQUAL expression_string
            | expression_string LESS_EQUAL expression_string
            '''
    if p[2] == '!=':
        p[0] = p[1] == p[3]
    elif p[2] == '==':
        p[0] = p[1] != p[3]
    elif p[2] == '<':
        p[0] = p[1] > p[3]
    elif p[2] == '>':
        p[0] = p[1] < p[3]
    elif p[2] == '<=':
        p[0] = p[1] >= p[3]
    elif p[2] == '>=':
        p[0] = p[1] <= p[3]

# ------------------------- Condicionales -------------------------

def p_else(p):
    'else : ELSE L_BRACE statements R_BRACE'
    p[0] = p[3]

def p_elif(p):
    'elif : ELIF L_PARENTHESIS  booleans R_PARENTHESIS L_BRACE statements R_BRACE'
    if p[3]:
        p[0] = p[6]

def p_elifs(p):
    '''elifs : elifs elif
            | elif
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        if p[1] is None:
            p[0] = p[2]
        elif p[2] is None:
            p[0] = p[1]
        else:
            p[0] = p[1] + [p[2]]

def p_if(p):
    '''if : IF L_PARENTHESIS  booleans R_PARENTHESIS L_BRACE statements R_BRACE
    '''
    if p[3]:
        p[0] = p[6]

def p_statement_if(p):
    '''statement :  if
                | if elifs
                | if elifs else
                '''
    if len(p) == 2:
        p[0] = p[1]

    elif len(p) == 3:
        if p[1] is not None:
            p[0] = p[1]
        elif p[1] is None and p[2] is not None:
            p[0] = p[2]

    elif len(p) == 4:
        if p[1] is not None:
            p[0] = p[1]
        elif p[1] is None and p[2] is not None:
            p[0] = p[2]
        else:  # p[1] is None and p[2] is None
            p[0] = p[3]

def p_statement_if_else(p):
    '''statement :  if else
                '''
    if p[1] is not None:
        p[0] = p[1]
    else:  # p[1] is None
        p[0] = p[2]

# ------------------------- Ciclo while -------------------------

def p_statement_while(p):
    'statement : loop_while'
    p[0] = p[1]

def p_loop_while(p):
    'loop_while : WHILE booleans L_BRACE statements  R_BRACE'
    i = 0
    stmts = []
    while p[2]:
        stmts.append(p[4])
        i = i + 1
        if (i == 20):
            print("Infinite loop")
            break
    p[0] = stmts

# ------------------------- Ciclo for -------------------------

# for(i=0 ar 9,azmozl=3){}
def p_for_loop(p):
    '''statement : FOR L_PARENTHESIS  NAME EQUALS expression TO expression COMMA STEP EQUALS expression R_PARENTHESIS L_BRACE statements R_BRACE'''
    stmts = []
    if p[7] > p[5]:
        i = 0
        while i < p[7] - p[5]:
            stmts.append(p[14])
            i = i + int(p[11])
        p[0] = stmts
    else:
        p[0] = "error :index {} > {}".format(p[5], p[7])

# for(i=0 ar 9){}
def p_for_loop2(p):
    '''statement : FOR L_PARENTHESIS  NAME EQUALS expression TO expression R_PARENTHESIS L_BRACE statements R_BRACE'''
    stmts = []
    if p[7] > p[5]:
        for i in range(p[7] - p[5]):
            stmts.append(p[10])
        p[0] = stmts
    else:
        p[0] = "erreur :index {} > {}".format(p[5], p[7])

# ------------------------- Funciones -------------------------

def p_argument_list(p):
    '''
        argument_list : expression
                    | argument_list COMMA expression
    '''
    stmts = []
    if (len(p) == 2):
        stmts.append(p[1])
    else:
        stmts.append(p[1])
        stmts.extend([p[3]])
    p[0] = stmts

def p_parameter(p):
    '''
    parameter : NAME
    '''
    p[0] = p[1]

def p_parameter_list(p):
    '''
        parameter_list : parameter
                    | parameter_list COMMA parameter
    '''
    stmts = []
    if (len(p) == 2):
        stmts.append(p[1])
    else:
        stmts.append(p[1])
        stmts.extend(p[3])
    p[0] = stmts

functions = {}

def p_func(p):
    '''statement : FUNCTION NAME L_BRACE statements R_BRACE
            | FUNCTION NAME L_BRACE statements return R_BRACE
            | FUNCTION  NAME LESS parameter_list GREATER L_BRACE statements R_BRACE
            | FUNCTION  NAME LESS parameter_list GREATER L_BRACE statements return R_BRACE
    '''
    if (len(p) == 6):
        functions[p[2]] = p[4]
    elif (len(p) == 9):
        functions[p[2]] = p[7]
    elif (len(p) == 7):
        functions[p[2]] = p[5]
    elif (len(p) == 10):
        functions[p[2]] = p[8]

def p_appel_func(p):
    '''
    statement : NAME L_PARENTHESIS argument_list R_PARENTHESIS  SEMICOLON
            | NAME L_PARENTHESIS  R_PARENTHESIS SEMICOLON

    '''
    if p[1] in functions:
        p[0] = functions[p[1]]
    else:
        p[0] = "function not declared !!"

def p_return(p):
    '''
    return : RETURN L_PARENTHESIS expression R_PARENTHESIS SEMICOLON
    '''
    p[0] = p[3]

# ------------------------- Error en caso de sintaxis -------------------------

def p_error(p):
    try:
        print(f"Syntax error at {p.value!r} ")
    except:
        print(f"Exception at {p.value!r} ")
parser = yacc.yacc()
