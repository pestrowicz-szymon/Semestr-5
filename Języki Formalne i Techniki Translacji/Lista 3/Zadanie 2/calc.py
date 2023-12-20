import ply.yacc as yacc
import ply.lex as lex
from enum import Enum

stack = []
p1 = 1234577
p2 = 1234576
flag = 0
p = 0
v = 0

class Sign(Enum):
    PLUS_VALUE = p1+1
    SUB_VALUE = p1+2
    NEG_VALUE = p1+3
    MUL_VALUE = p1+4
    DIV_VALUE = p1+5
    POW_VALUE = p1+6

tokens = (
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
    'POWER',
    'COMMENT'
)

t_PLUS      = r'\+'
t_MINUS     = r'-'
t_TIMES     = r'\*'
t_DIVIDE    = r'/'
t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_POWER     = r'\^'
t_COMMENT   = r'\#.*'

def t_NUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

t_ignore  = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value) 

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
 
lexer = lex.lex()

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'POWER', 'UMINUS'),            
)

def p_statement_expr(t):
    'statement : expression'
    global flag, p, v
    if(flag==-1):
        print("", end='');
        print("> "+ str(v) + " nie jest odwracalne modulo "+ str(p));
        stack.clear()
    else:
        print_stack()
        print("= %d" %t[1])
        flag = 0
    flag = 0

def p_statement_comment(t):
    'statement : COMMENT'

def p_expression(t):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression POWER expression1'''           
    if t[2] == '+': t[0] = add(t[1], t[3], p1);     stack.append([Sign.PLUS_VALUE.value, p1])
    elif t[2] == '-': t[0] = sub(t[1], t[3], p1);   stack.append([Sign.SUB_VALUE.value, p1])
    elif t[2] == '*': t[0] = mul(t[1], t[3], p1);   stack.append([Sign.MUL_VALUE.value, p1])
    elif t[2] == '/':
        t[0] = div(t[1], t[3], p1)
        if(t[0]==-1):
            global flag, p, v
            flag = -1
            p = p1
            v = t[3]
        else:
              stack.append([Sign.DIV_VALUE.value, p1])
    elif t[2] == '^': t[0] = power(t[1], t[3], p1); stack.append([Sign.POW_VALUE.value, p1])

def p_expression1(t):
    '''expression1 : expression1 PLUS expression1
                   | expression1 MINUS expression1
                   | expression1 TIMES expression1
                   | expression1 DIVIDE expression1''' 
    if t[2] == '+': t[0] = add(t[1], t[3], p2);   stack.append([Sign.PLUS_VALUE.value, p2])
    elif t[2] == '-': t[0] = sub(t[1], t[3], p2); stack.append([Sign.SUB_VALUE.value, p2])
    elif t[2] == '*': t[0] = mul(t[1], t[3], p2); stack.append([Sign.MUL_VALUE.value, p2])
    elif t[2] == '/':
        t[0] = div(t[1], t[3], p2)
        if(t[0]==-1):
            global flag, p, v
            flag = -1
            p = p2
            v = t[3]
        else:
            stack.append([Sign.DIV_VALUE.value, p2])

def p_expression_group(t):
    'expression : LPAREN expression RPAREN'
    t[0] = t[2]

def p_expression_number(t):
    'expression : NUMBER'
    t[0] = t[1]%p1; stack.append([t[0], p1]) 

def p_expression_uminus(t):
    'expression : MINUS expression %prec UMINUS'
    t[0] = p1 - t[2]; stack.append([Sign.NEG_VALUE.value, p1])

def p_expression1_group(t):
    'expression1 : LPAREN expression1 RPAREN'
    t[0] = t[2]

def p_expression1_number(t):
    'expression1 : NUMBER'
    t[0] = t[1]%p2; stack.append([t[0], p2])

def p_expression1_uminus(t):
    'expression1 : MINUS expression1 %prec UMINUS'
    t[0] = p2 - t[2]; stack.append([Sign.NEG_VALUE.value, p2])

def p_error(t):
    print("Syntax error at '%s'" % t.value)

def print_stack():
    i = 0
    while(i < len(stack)):
        if (stack[i][0] < p1):
            if (i+1<len(stack) and stack[i+1][0]==Sign.NEG_VALUE.value):
                print(stack[i][1]-stack[i][0]," ", end='')
                i+=2
            else:
                print(stack[i][0]," " , end='')
                i+=1
        else:
            if (stack[i][0]==Sign.PLUS_VALUE.value):
                print("+ ", end='')
            elif (stack[i][0]==Sign.SUB_VALUE.value):
                print("- ", end='')
            elif (stack[i][0]==Sign.NEG_VALUE.value):
                print("~ ", end='')
            elif (stack[i][0]==Sign.MUL_VALUE.value):
                print("* ", end='')
            elif (stack[i][0]==Sign.DIV_VALUE.value):
                print("/ ", end='')
            elif (stack[i][0]==Sign.POW_VALUE.value):
                print("^ ", end='')
            i+=1
    stack.clear()

def add(a, b, p):
    return (a + b)%p

def sub(a, b, p):
    return (a - b)%p

def mul(a, b, p):
    return (a * b)%p

def power(a, b, p):
    return pow(a, b, p)

def div(a, b, p):
    g, x, y = gcdExtended(b, p)
    if (g != 1):
        inv = -1
    else:
        inv = (x%p + p) % p
    a = a % p
    if (inv == -1):
        return -1
    return (inv * a) % p

def gcdExtended(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = gcdExtended(b%a, a)
    x = y1 - (b//a) * x1
    y = x1
    return gcd, x, y

parser = yacc.yacc()
yacc.yacc(method="LALR")


def main():
    while True:
        try:
            result_text = ""
            s = input('> ')
            while len(s) > 0 and s[-1] ==  "\\":
                result_text += s[:1]
                s = input('> ')
            result_text += s + "\n"
        except EOFError:
            break
        else:
            parser.parse(s)

if __name__ == '__main__':
    main()