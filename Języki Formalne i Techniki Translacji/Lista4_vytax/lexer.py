from sly import Lexer


class MyLexer(Lexer):
    tokens = { # words that appear in alnguage spec
        'PROCEDURE', 
        'PROGRAM', 
        'IS', 
        'IN', 
        'END', 
        'IF', 
        'THEN', 
        'ELSE', 
        'ENDIF', 
        'WHILE', 
        'DO', 
        'ENDWHILE',
        'REPEAT', 
        'UNTIL', 
        'READ', 
        'WRITE', 
        'ASSIGN', 
        'EQ', 
        'NEQ', 
        'GT', 
        'LT', 
        'GE', 
        'LE', 
        'PIDENTIFIER', 
        'NUM'
        }

    literals = {';', 
                ',', 
                '(', 
                ')', 
                '[', 
                ']', 
                'T',
                '+', 
                '-',
                '*', 
                '/', 
                '%'}

    ignore = ' \t'
    ignore_comment = r'\#.*'
    ignore_newline = r'\n+'

    PROCEDURE = r'PROCEDURE'
    PROGRAM = r'PROGRAM'
    IS = r'IS'
    IN = r'IN'
    IF = r'IF'
    THEN = r'THEN'
    ELSE = r'ELSE'
    ENDIF = r'ENDIF'
    WHILE = r'WHILE'
    DO = r'DO'
    ENDWHILE = r'ENDWHILE'
    END = r'END'
    REPEAT = r'REPEAT'
    UNTIL = r'UNTIL'
    READ = r'READ'
    WRITE = r'WRITE'

    ASSIGN = r':='
    NEQ = r'!='
    GE = r'>='
    LE = r'<='
    EQ = r'='
    GT = r'>'
    LT = r'<'

    PIDENTIFIER = r'[_a-z]+'

    @_(r'[0-9]+')
    def NUM(self, t):
        t.value = int(t.value)
        return t

    def error(self, t):
        print(f'ERROR: Unknown symbol \"{t.value[0]}\"')
        exit(2)
