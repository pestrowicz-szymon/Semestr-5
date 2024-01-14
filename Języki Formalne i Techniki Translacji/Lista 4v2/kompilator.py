from sly import Lexer, Parser
import CodeGenerator
import sys

class MyLexer(Lexer):
    tokens = {
        # words that appear in language spec
        'PROCEDURE', 'IS', 'IN', 'END', 'PROGRAM', 'IF', 'THEN', 'ELSE', 'ENDIF', 'WHILE', 'DO', 'ENDWHILE', 
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
        'SEMICOLON', # srednik
        'LPAREN', # (
        'RPAREN', # )
    }

    ignore = ' \t'
    ignore_comment = r'\#(.*?(\\\n)*)+\n'
    ignore_newline = r'\n+'

    PROCEDURE = r'PROCEDURE'
    IS = r'IS'
    IN = r'IN'
    END = r'END'
    PROGRAM = r'PROGRAM'
    IF = r'IF'
    THEN = r'THEN'
    ELSE = r'ELSE'
    ENDIF = r'ENDIF'
    WHILE = r'WHILE'
    DO = r'DO'
    ENDWHILE = r'ENDWHILE'
    REPEAT = r'REPEAT'
    UNTIL = r'UNTIL'
    READ = r'READ'
    WRITE = r'WRITE'
    T = r'T'

    ADD = r'\+'
    SUB = r'\-'
    MUL = r'\*'
    DIV = r'/'
    MOD = r'%'
    ASS = r':='
    COMA =r','

    EQ = r'='
    NEQ = r'!='
    GT = r'>'
    LT = r'<'
    GEQ = r'>='
    LEQ = r'<='

    SEMICOLON = r';'
    LPAREN = r'\('
    RPAREN = r'\)'

    NUM = r'\d+'
    PIDENTIFIER = r'[_a-z]+'

class MyParser(Parser):
    tokens = MyLexer.tokens
    #symbols = SymbolTable()
    code = None
    # We need a set of consts that will be written inside a loop/if. These need to be generated and stored pre-entry
    # because the entry might not happen at all, for instance for [if 1 > 2 then write 1; endif write 1;] the code
    # for storing 1 in memory would get generated inside the if and never be executed, causing the second write to
    # print something undefined.
    consts = set()

    def __init__(self):
        self.result = []

    @_('main')
    def program_all(self, p):
        pass
    
    @_('PROGRAM IS declarations IN commands END',
       'PROGRAM IS IN commands END')
    def main(self, p):
        self.result.append('MAIN')

    @_('commands command',
       'command')
    def commands(self, p):
        self.result.append('COMMANDS')

    @_('PIDENTIFIER')
    def command(self, p):
        self.result.append('COMMAND' + p[0])

    @_('declarations COMA PIDENTIFIER',
       'PIDENTIFIER')
    def declarations(self, p):
        self.result.append('DECLARATIONS')

    
lexer = MyLexer()
parser = MyParser()
with open(sys.argv[1]) as in_f:
    text = in_f.read()

parser.parse(lexer.tokenize(text))
result = parser.result
#code_gen = parser.code
#code_gen.gen_code()
with open(sys.argv[2], 'w') as out_f:
    #for line in code_gen.code:
        #print(line, file=out_f)
    for line in result:
        print(line, file=out_f)
    #print(result, file=out_f)