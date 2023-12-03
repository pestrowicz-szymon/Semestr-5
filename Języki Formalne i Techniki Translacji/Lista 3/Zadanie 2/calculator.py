SIZE = 1234577
expression = ""


def valueFromField(n):
    result = int(n % SIZE)
    if result < 0:
        result += SIZE
    return result


def valueFromFieldForExp(n):
    result = int(n % (SIZE - 1))
    if result < 0:
        result += SIZE - 1
    return result


def inverse(n):
    t = 0
    r = SIZE
    newt = 1
    newr = valueFromField(n)

    while newr != 0:
        quotient = int(r / newr)

        curr = newt
        newt = t - quotient * newt
        t = curr

        curr = newr
        newr = r - quotient * newr
        r = curr

    return valueFromField(t)


tokens = (
    'NUM',
    'PLUS',
    'MINUS',
    'MULTIPLY',
    'DIVIDE',
    'POW',
    'LBRACKET',
    'RBRACKET',
    'COMMENT'
)

t_PLUS       = r'\+'
t_MINUS      = r'-'
t_MULTIPLY   = r'\*'
t_DIVIDE     = r'/'
t_POW        = r'\^'
t_LBRACKET   = r'\('
t_RBRACKET   = r'\)'

t_ignore = " \t"


def t_COMMENT(t):
    r'\#.*'
    pass


def t_NUM(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    global expression


import ply.lex as lex
lexer = lex.lex()

precedence = (
    ('left', 'PLUS'),
    ('left', 'MINUS'),
    ('left', 'MULTIPLY'),
    ('left', 'DIVIDE'),
    ('right', 'POW'),
    ('right', 'UMINUS')
)


def p_statement_empty(t):
    'statement : '
    pass


def p_statement_expr(t):
    'statement : expression'
    global expression
    print(expression)
    print('Result :', valueFromField(t[1]))
    expression = ""


def p_expression_plus(t):
    'expression : expression PLUS expression'
    t[0] = valueFromField(t[1] + t[3])
    global expression
    expression += '+ '


def p_expression_minus(t):
    'expression : expression MINUS expression'
    t[0] = valueFromField(t[1] - t[3])
    global expression
    expression += '- '


def p_expression_multiply(t):
    'expression : expression MULTIPLY expression'
    t[0] = valueFromField(t[1] * t[3])
    global expression
    expression += '* '


def p_expression_divide(t):
    'expression : expression DIVIDE expression'
    t[0] = valueFromField(t[1] * inverse(t[3]))
    global expression
    expression += '/ '


def p_expression_pow(t):
    'expression : expression POW NUM'
    t[0] = valueFromField(valueFromField(t[1]) ** valueFromFieldForExp(t[3]))
    global expression
    expression += str(valueFromFieldForExp(t[3])) + ' ^ '


def p_expression_pow_with_minus(t):
    'expression : expression POW MINUS NUM %prec UMINUS'
    t[0] = valueFromField(valueFromField(t[1]) ** valueFromFieldForExp(-t[4]))
    global expression
    expression += str(valueFromFieldForExp(-t[4])) + ' ^ '


def p_expression_uminus(t):
    'expression : MINUS NUM %prec UMINUS'
    t[0] = valueFromField(-t[2])
    global expression
    expression += str(t[0]) + " "


def p_expression_group(t):
    'expression : LBRACKET expression RBRACKET'
    t[0] = t[2]


def p_expression_num(t):
    'expression : NUM'
    t[0] = valueFromField(t[1])
    global expression
    expression += str(t[0]) + " "


def p_error(t):
    print('Error')
    global expression
    expression = ""


import ply.yacc as yacc
parser = yacc.yacc()


def isLineContinuation(line):
    return len(line) >= 2 and line[-1] == '\\' and line[-2] != '\\'


line = ""

while True:
    try:
        line += input('')
    except EOFError:
        break

    if isLineContinuation(line):
        line = line[:-1]
    else:
        parser.parse(line)
        line = ""