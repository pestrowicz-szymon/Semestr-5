from sly import Lexer

class MyLexer(Lexer):
    tokens = {
        # words that appear in language spec
        'PROCEDURE', 'IS', 'IN', 'ENDIF', 'END', 'PROGRAM', 'IF', 'THEN', 'ELSE', 'WHILE', 'DO', 'ENDWHILE', 
        'REPEAT', 'UNTIL', 'READ', 'WRITE', 'PIDENTIFIER', 'T', 'NUM', # number 
        'PIDENTIFIER', # name of function/table/variable
        # expressions 
        'ADD', # addition
        'SUB', # substraction
        'MUL', # multiplication
        'DIV', # division
        'MOD', # modulo division
        'ASS', # assign value to pidentifier
        'COMA',# ,
        # conditions
        'EQ',  # is equal
        'NEQ', # is not equal
        'GT',  # is greater than
        'LT',  # is less than
        'GEQ', # is greater or equal
        'LEQ', # is less or equal
        # rest
        #'SEMICOLON', # srednik
        'LPAREN', # (
        'RPAREN', # )
        'LBRACK', # [
        'RBRACK', # ]
    }

    literals = {';', ',', '(', ')', '[', ']', 'T',
                '+', '-', '*', '/', '%'}

    ignore = ' \t'
    ignore_comment = r'\#(.*?(\\\n)*)+\n'
    ignore_newline = r'\n+'

    PROCEDURE = r'PROCEDURE'
    IS = r'IS'
    IN = r'IN'
    ENDIF = r'ENDIF'
    PROGRAM = r'PROGRAM'
    IF = r'IF'
    THEN = r'THEN'
    ELSE = r'ELSE'
    WHILE = r'WHILE'
    DO = r'DO'
    ENDWHILE = r'ENDWHILE'
    REPEAT = r'REPEAT'
    UNTIL = r'UNTIL'
    READ = r'READ'
    WRITE = r'WRITE'
    T = r'T'
    END = r'END'

    ADD = r'\+'
    SUB = r'\-'
    MUL = r'\*'
    DIV = r'/'
    MOD = r'%'
    ASS = r':='
    COMA =r','

    NEQ = r'!='
    GEQ = r'>='
    LEQ = r'<='
    GT = r'>'
    LT = r'<'
    EQ = r'='

    #SEMICOLON = r';'
    LPAREN = r'\('
    RPAREN = r'\)'
    LBRACK = r'\['
    RBRACK = r'\]'

    NUM = r'\d+'
    PIDENTIFIER = r'[_a-z]+'