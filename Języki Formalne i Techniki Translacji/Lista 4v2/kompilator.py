from sly import Lexer, Parser
import CodeGenerator
import sys

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

    ignore = ' \t'
    ignore_comment = r'\#(.*?(\\\n)*)+\n'
    ignore_newline = r'\n+'
    ignore_semicolon = r';'

    PROCEDURE = r'PROCEDURE'
    IS = r'IS'
    IN = r'IN'
    ENDIF = r'ENDIF'
    END = r'END'
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

    #SEMICOLON = r';'
    LPAREN = r'\('
    RPAREN = r'\)'
    LBRACK = r'\['
    RBRACK = r'\]'

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
        self.result.append('PROGRAM ALL')

    #@_('procedures PROCEDURE proc_head IS declarations IN commands END',
    #   'procedures PROCEDURE proc_head IS IN commands END')
    #def procedures(self, p):
    #    self.result.append('PROCEDURES')
    
    @_('PROGRAM IS declarations IN commands END',
       'PROGRAM IS IN commands END')
    def main(self, p):
        self.result.append('MAIN')

    @_('commands command',
       'command')
    def commands(self, p):
        #self.result.append('COMMANDS')
        pass

    @_('identifier ASS expression',
       'IF condition THEN commands ENDIF',
       'IF condition THEN commands ELSE commands ENDIF',
       'WHILE condition DO commands ENDWHILE',
       'REPEAT commands UNTIL condition',
       'proc_call',
       'READ identifier',
       'WRITE value')
    def command(self, p):
        self.result.append('COMMAND ' + p[0])

    #@_('PIDENTIFIER LPAREN args_decl RPAREN')
    #def proc_head(self, p):
    #    self.result.append("PROC_HEAD")

    @_('PIDENTIFIER LPAREN args RPAREN')
    def proc_call(self, p):
        self.result.append('PROC_CALL')

    @_('declarations COMA PIDENTIFIER',
       'declarations COMA PIDENTIFIER LBRACK NUM RBRACK',
       'PIDENTIFIER',
       'PIDENTIFIER LBRACK NUM RBRACK')
    def declarations(self, p):
        self.result.append('DECLARATIONS ' + p.PIDENTIFIER)

    #@_('args_decl COMA PIDENTIFIER',
    #   'args_decl COMA T PIDENTIFIER',
    #   'PIDENTIFIER',
    #   'T PIDENTIFIER')
    #def args_decl(self, p):
    #    self.result.append('ARGS_DECL')

    @_('args COMA PIDENTIFIER',
       'PIDENTIFIER')
    def args(self, p):
        self.result.append('ARGS')

    @_('value',
       'value ADD value',
       'value SUB value',
       'value MUL value',
       'value DIV value',
       'value MOD value',
       'value ASS value') # maybe it shouldnt be there, idk
    def expression(self, p):
        self.result.append('EXPRESSION ' + p[0] + ' ' + p[1] + ' ' + p[2])

    @_('value EQ value',
       'value NEQ value',
       'value GT value',
       'value LT value',
       'value GEQ value',
       'value LEQ value')
    def condition(self, p):
        self.result.append('CONDITION ' + p[0] + ' ' + p[1] + ' ' + p[2])

    @_('NUM',
       'identifier')
    def value(self, p):
        self.result.append('VALUE ' + p[0])
        return p[0]

    @_('PIDENTIFIER',
       'PIDENTIFIER LBRACK NUM RBRACK',
       'PIDENTIFIER LBRACK PIDENTIFIER RBRACK')
    def identifier(self, p):
        self.result.append('IDENTIFIER ' + ' '.join(p))
        return ' '.join(p)

    
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