import parser

with open('pruebas/testCompleto.txt', 'r') as file:
    data = file.read()
    result = parser.parser.parse(data)

if result is not None:
    for r in result:
        if r is not None:
            if isinstance(r, list):
                for i in r:
                    if i is not None:
                        print(i)
            else:
                print(r)
