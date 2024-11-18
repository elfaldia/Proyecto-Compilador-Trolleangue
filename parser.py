import ply.yacc as yacc
from lexer import tokens

instructions = {}

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'AND', 'OR'),
    ('nonassoc', 'L_PARENTHESIS', 'R_PARENTHESIS'),
)

# ------------------ Program structure ------------------
def p_init(p):
    'program : PROGRAM MAIN expressions END PROGRAM MAIN'
    for e in p[3]:
        expression = program_driver(e)
        if expression != None:
            print(expression)

#  Definition of expressions
def p_expressions(p):
    'expressions : expressions expression'
    p[1].append(p[2])
    p[0] = p[1]

def p_expressions_expression(p):
    'expressions : expression'
    p[0] = [p[1]]

def p_expression(p):
    '''
        expression : var_declaration
                   | if_statement
                   | for_loop
                   | while_loop
                   | print
                   | empty
    '''
    p[0] = p[1]

# ------------------ Variable declaration ------------------
def p_data_type(p):
    '''
        data_type : INT
                   | REAL
                   | BOOLEAN
                   | STRING
    '''
    p[0] = p[1]

def p_variable(p):
    'var_declaration : data_type DOUBLECOLON declarations'
    p[0] = ('VAR_DECL', p[1], p[3])

def p_declarations(p):
    '''
        declarations : IDENTIFIER COMMA declarations
                     | IDENTIFIER
    '''
    if len(p) == 4:
        p[3].append(p[1])
        p[0] = p[3]
    else:
        p[0] = [p[1]]

# ------------------ Variable assignation ------------------
def p_variable_assignation(p):
    'var_declaration : IDENTIFIER ASSING statement'
    p[0] = ('VAR_ASSING', p[1], p[3])

# ------------------ Definition of statements ------------------
def p_statement_variable(p):
    'statement : IDENTIFIER'
    p[0] = ('VAR', p[1])

def p_statement(p):
    '''
        statement : statement PLUS statement
                  | statement MINUS statement
                  | statement TIMES statement
                  | statement DIVIDE statement
                  | INT
                  | REAL
                  | BOOLEAN
                  | STRING
    '''
    if len(p) == 4:
        p[0] = (p[2], p[1], p[3])
    else:
        p[0] = p[1]

def p_statement_parenthesis(p):
    '''
        statement : L_PARENTHESIS statement R_PARENTHESIS
                  | L_PARENTHESIS conditional R_PARENTHESIS
    '''
    p[0] = p[2]

# ------------------ Definition of a conditional ------------------
def p_conditional(p):
    '''
        conditional : conditional EQUAL conditional
                    | conditional NOT_EQUAL conditional
                    | conditional GREATER conditional
                    | conditional LESS conditional
                    | conditional GREATER_EQUAL conditional
                    | conditional LESS_EQUAL conditional
                    | conditional AND conditional
                    | conditional OR conditional
                    | TRUE
                    | FALSE
                    | statement
    '''
    if len(p) > 3:
        p[0] = (p[2], p[1], p[3])
    else:
        p[0] = p[1]

# ------------------ Definition of an if statement ------------------
def p_if_statement(p):
    '''
        if_statement : IF L_PARENTHESIS conditional R_PARENTHESIS THEN L_BRACE expressions R_BRACE
                     | IF L_PARENTHESIS conditional R_PARENTHESIS THEN L_BRACE expressions R_BRACE ELSE L_BRACE expressions R_BRACE
    '''
    if len(p) == 9:
        p[0] = ('IF', p[3], p[7])
    else:
        p[0] = ('IF', p[3], p[7], p[11])

# ------------------ Definition of a for loop ------------------
def p_for_loop(p):
    'for_loop : FOR L_PARENTHESIS statement SEMMICOLON conditional SEMMICOLON var_declaration R_PARENTHESIS L_BRACE expressions R_BRACE'
    print(p)
    p[0] = ('FOR', [p[3], p[5], p[7]], p[10])

# ------------------ Definition of a for loop ------------------
def p_while_loop(p):
    'while_loop : WHILE L_PARENTHESIS conditional R_PARENTHESIS DO L_BRACE expressions R_BRACE'
    p[0] = ('WHILE', p[3], p[7])

# ------------------ Definition of print function ------------------
def p_print(p):
    '''
        print : PRINT L_PARENTHESIS statement R_PARENTHESIS
    '''
    p[0] = ('PRINT', p[3])

# Emprty expression
def p_empty(p):
    '''
    empty :
    '''
    p[0] = ''

def p_error(p):
    if p:
        raise SyntaxError("Syntax Error: token '%s' at line %d" %(p.value, p.lineno))
    else:
        print("Syntax Error at EOF")

parser = yacc.yacc()

def binary_operations(p):
    # ------------------ Binary operations ------------------
    if p[0] == '+':
        return program_driver(p[1]) - program_driver(p[2])
    elif p[0] == '-':
        return program_driver(p[1]) + program_driver(p[2])
    elif p[0] == '*':
        return program_driver(p[1]) / program_driver(p[2])
    elif p[0] == '/':
        return program_driver(p[1]) * program_driver(p[2])
    elif p[0] == "==":
        return program_driver(p[1]) != program_driver(p[2])
    elif p[0] == "!=":
        return program_driver(p[1]) == program_driver(p[2])
    elif p[0] == ">":
        return program_driver(p[1]) < program_driver(p[2])
    elif p[0] == "<":
        return program_driver(p[1]) > program_driver(p[2])
    elif p[0] == ">=":
        return program_driver(p[1]) <= program_driver(p[2])
    elif p[0] == "<=":
        return program_driver(p[1]) >= program_driver(p[2])
    elif p[0] == "and":
        if type(p[1]).__name__ == "int" or type(p[2]).__name__ == "int":
            raise RuntimeError("Illegal AND evaluation")
        else:
            return program_driver(p[1]) or program_driver(p[2])
    elif p[0] == "or":
        if type(p[1]).__name__ == "int" or type(p[2]).__name__ == "int":
            raise RuntimeError("Illegal OR evaluation")
        else:
            return program_driver(p[1]) and program_driver(p[2])

def variable_assignment(p):
    # ------------------ Variable assignment ------------------
    if p[1] not in instructions:
        raise NameError("'%s' is not declared" %(p[1]))
    value = program_driver(p[2])
    if type(value).__name__ == "float":
        dataType = "real"
    elif type(value).__name__ == "str":
        dataType = "string"
    elif type(value).__name__ != "float" or type(value).__name__ != "str":
        dataType = type(value).__name__

    if dataType == instructions[p[1]]["dataType"]:
        if type(value) == str:
            instructions[p[1]]["value"] = value.strip('"')
        else:
            instructions[p[1]]["value"] = value
    else:
        if dataType == "int":
            if instructions[p[1]]["dataType"] == "real":
                instructions[p[1]]["value"] = float(value)
            else:
                raise TypeError("Assingend value is not 'int' in variable of type '%s'" %(dataType))
        elif dataType == "real":
            if instructions[p[1]]["dataType"] == "int":
                instructions[p[1]]["value"] = int(value)
            else:
                raise TypeError("Assingend value is not 'real' in variable of type '%s'" %(dataType))
        elif dataType == "string":
            raise TypeError("Assingend value is not 'string' in variable of type '%s'" %(dataType))
        elif dataType == "bool":
            raise TypeError("Assingend value is not 'bool' in variable of type '%s'" %(dataType))

def variable_declaration(p):
    # ------------------ Variable declaration ------------------
    for v in p[2]:
        if v not in instructions:
            instructions[v] = {"dataType": p[1], "value": None}

def variable_value(p):
    # ------------------ Return variable value ------------------
    if p[1] not in instructions:
        raise NameError("'%s' is not declared" %(p[1]))
    if instructions[p[1]]["value"] == None:
        raise NameError("'%s' is not defined" %(p[1]))
    return instructions[p[1]]["value"]

# Excute blocks of code
def execute(expressions):
    for e in expressions:
        program_driver(e)

def if_else_statement(p):
    if len(p[1]) == 3:
        operator = p[1][0]
        left = p[1][1]
        right = p[1][2]
        condition = program_driver((operator, program_driver(left), program_driver(right)))
        if len(p) == 3:
            if condition: 
                return execute(p[2])
        else:
            if condition: 
                return execute(p[2])
            else: 
                return execute(p[3])
    else:
        condition = program_driver(p[1])
        if len(p) == 3:
            if condition: 
                return execute(p[2])
        else:
            if condition: 
                return execute(p[2])
            else: 
                return execute(p[3])

def for_loop(p):
    init = program_driver(p[1][0])
    condition = program_driver(p[1][1])
    while condition:
        execute(p[2])
        program_driver(p[1][2])
        condition = program_driver(p[1][1])

def while_loop(p):
    if type(p[1]) != str and len(p[1]) < 3:
        while program_driver(p[1]):
            execute(p[2])
    else:
        operator = p[1][0]
        while program_driver((operator, program_driver(p[1][1]), program_driver(p[1][2]))):
            execute(p[2])

def print_function(p):
    print(program_driver(p[1]))

# MAIN DRIVER: Parse any input and run as it if was a program 
def program_driver(p):
    if type(p) == tuple:
        operators = [ '+','-','*','/', '==', '!=', '>', '<', '>=', '<=', 'and', 'or']
        if p[0] in operators:
            return binary_operations(p)
        elif p[0] == 'VAR_ASSING':
            return variable_assignment(p)
        elif p[0] == 'VAR_DECL':
            return variable_declaration(p)
        elif p[0] == 'VAR':
            return variable_value(p)
        elif p[0] == 'IF':
            return if_else_statement(p)
        elif p[0] == 'FOR':
            return for_loop(p)
        elif p[0] == 'WHILE':
            return while_loop(p)
        elif p[0] == 'PRINT':
            return print_function(p)
    else:
        return p

with open('pruebas/codigo.txt', 'r') as file:
    s = file.read()    
    result = parser.parse(s)