from sly import Lexer

class MyLexer(Lexer):
    ignore = ' \t' #ignore whitespaces
    ignore_comment = r'\#(.*?(\\\n)*)+\n' #ignore comments

    tokens = {
        # words that appear in language spec
        'PROCEDURE',
        'IS',
        'IN',
        'END',
        'PROGRAM',
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
        'WRITE'
        'PIDENTIFIER',
        'T',   
        'NUM', # number,
        'PIDENTIFIER', # name of function/table/variable
        # expressions 
        'ADD', # addition
        'SUB', # substraction
        'MUL', # multiplication
        'DIV', # division
        'MOD', # modulo division
        # conditions
        'EQ',  # is equal
        'NEQ', # is not equal
        'GT',  # is greater than
        'LT',  # is less than
        'GEQ', # is greater or equal
        'LEQ', # is less or equal
        # rest
        'SEMICOLON', # srednik
        'LPAREN', # (
        'RPAREN', # )


    }

    t_PROCEDURE = r'PROCEDURE'
    t_IS = r'IS',
    t_IN = r'IN',
    t_END = r'END',
    t_PROGRAM = r'PROGRAM',
    t_IF = r'IF',
    t_THEN = r'THEN',
    t_ELSE = r'ELSE',
    t_ENDIF = r'ENDIF',
    t_WHILE = r'WHILE',
    t_DO = r'DO',
    t_ENDWHILE = r'ENDWHILE',
    t_REPEAT = r'REPEAT',
    t_UNTIL = r'UNTIL',
    t_READ = r'READ',
    t_WRITE = r'WRITE'
    t_PIDENTIFIER = r'PIDENTIFIER',
    t_T = r'T',
    t_NUM = r'\d+'
    t_PIDENTIFIER = r'[_a-z]+'

    t_ADD = r'\+',
    t_SUB = r'\-',
    t_MUL = r'\*',
    t_DIV = r'/',
    t_MOD = r'%',

    t_EQ = r'=',
    T_NEQ = r'!=',
    t_GT = r'>',
    t_LT = r'<',
    t_GEQ = r'>=',
    t_LEQ = r'<=',

    t_SEMICOLON = r';',
    t_LPAREN = r'\(',
    t_RPAREN = r'\)'



     