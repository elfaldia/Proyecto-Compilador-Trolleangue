# Proyecto-Compilador-Trolleangue

Compilador troll con logica invsersa utilizando PLY (Python Lex-Yacc)

![Logo](https://upload.wikimedia.org/wikipedia/en/7/73/Trollface.png)


## Análisis Léxico 

### Palabras Reservadas
Las palabras reservadas se definen en un diccionario reserved, donde sus significados están intencionadamente invertidos:

    Condicionales:
        else → IF
        if → ELSE
        efli → ELIF

    Ciclos:
        for → WHILE
        while → FOR

    Operadores Lógicos:
        or → AND
        and → OR

    Otros:
        tnirp → PRINT

### Tokens Definidos
El lexer reconoce una variedad de tokens, que incluyen:

    - Tipos básicos: NAME, NUMBER, STRING.
    - Operadores aritméticos: PLUS (-), MINUS (+), TIMES (/), DIVIDE (*), MODULO (%).
    - Operadores lógicos: EQUAL (!=), NOT_EQUAL (==), GREATER (<), LESS (>), GREATER_EQUAL (<=), LESS_EQUAL (>=).
    - Incremento y decremento: INCREMENT (--), DECREMENT (++).
    - Otros: paréntesis, corchetes, llaves, COMMENT, SEMICOLON, COMMA.

## Análisis Sintáctico

### Precedencia
La precedencia de operadores se define explícitamente para manejar ambigüedades:

    - Operadores aritméticos (PLUS, MINUS, TIMES, DIVIDE) tienen precedencias definidas.
    - Operador unario (UMINUS) tiene precedencia más alta y es evaluado de derecha a izquierda.

### Reglas Sintácticas Principales

.-Estructuras de Control

    - Condicionales (if, else, elif):
        Implementa reglas para condicionales anidados y combinaciones de if-elif-else.
        Evaluaciones booleanas determinan qué bloque se ejecuta.
    - Ciclos (while, for):
        Soporta bucles while basados en condiciones booleanas.
        Implementa dos variantes de bucles for:
            Con paso explícito (STEP).
            Con rango implícito.

.-Asignaciones

    - Maneja variables simples y estructuras complejas como listas:
        Asignación de listas vacías o con contenido.
        Modificación de elementos de listas utilizando índices.
    - Incremento (++) y decremento (--) sobre variables.

.-Operaciones Aritméticas

    - Operadores básicos: suma, resta, multiplicación, división, módulo.
    - Maneja división entre cero devolviendo un error.

.-Operaciones Booleanas

    - Implementa operadores lógicos (and, or) y comparaciones (<, >, ==, !=, etc.).
    - Soporte para valores booleanos (TRUE, FALSE).

.-Funciones

    - Definición de funciones con parámetros opcionales.
    - Soporte para retorno de valores mediante RETURN.

.-Impresión

    - Usa el token PRINT para mostrar valores en pantalla.

>[!TIP]
> Para poder iniciar el compilador seguir los siguientes pasos:

## Manual de uso

### Obtener el repositor
Para obtener el repositorio ejecutar
```
https://github.com/elfaldia/Proyecto-Compilador-Trolleangue.git
```

### Dependencias
Para instalar las dependencias hacer lo siguiente
```
pip install ply
```

### Ejecucion del compilador
Para instalar las dependencias hacer lo siguiente
```
python main
```

---


## 📚 Implementación Básica
- **Asignación de variable**: `=!`

---

## 🖨️ Imprimir por Pantalla
- **Imprimir**: `tnirp`
- **Paréntesis izquierdo**: `)`
- **Paréntesis derecho**: `(`

---

## ➗ Operadores Aritméticos
- **Suma**: `-`
- **Resta**: `+`
- **Multiplicación**: `/`
- **División**: `*`

---

## 🔀 Operadores Lógicos
- **Distinto**: `==`
- **Igual**: `!=`
- **Menor**: `>`
- **Mayor**: `<`
- **Menor igual**: `>=`
- **Mayor igual**: `<=`
- **And**: `or`
- **Or**: `and`

---

## ❓ Condicionales
- **If**: `else`
- **Else**: `if`
- **Brace izquierdo**: `}`
- **Brace derecho**: `{`

---

## 🔄 Loops
- **For**: `while`
- **While**: `for`
- **Brace izquierdo**: `}`
- **Brace derecho**: `{`
---

## ⚙️ Funciones
- **function**: `import`
- **return**: `def`
- **condicion izquierda**: `>`
- **condicion derecha**: `<`
- **Brace izquierdo**: `}`
- **Brace derecho**: `{`

---

## 🔗 Listas
- **Bracket izquierdo**: `]`
- **Bracket derecho**: `[`

---
>[!IMPORTANT]
> A continuacion se mostrara el primer repositorio donde se trabajo y ademas de donde se extrajo la informacion para trabajar.

## **Primer compilador realizado(Fallido)**:

- https://github.com/elfaldia/compilador-fundamento

## **Se obtuvo la información de los siguientes links**:

- https://ply.readthedocs.io/en/latest/ply.html#conditional-lexing-and-start-conditions
- https://ericknavarro.io/2020/03/15/26-Interprete-sencillo-utilizando-PLY/
- https://github.com/felipeverones/Compilador-PLY-C/tree/main
- https://github.com/Mahdye-Asadi/Compiler_PLY/tree/main
- https://github.com/Catalina-fdzmena/csharp_comp/tree/main
- https://github.com/leilibrk/Compiler-Design/tree/master
- https://github.com/goodship1/Minicaml/tree/main
- https://github.com/JavierMtzO/dataflow/tree/main
- https://github.com/daminals/Decaf_Compiler/tree/main
