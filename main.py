import parser

with open('pruebas/codigo.txt', 'r') as file:
    s = file.read()
    result = parser.parser.parse(s)