from sly import Lexer, Parser
from symbol_table import SymbolTable
from code_generator import CodeGenerator
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

class MyParser(Parser):
    tokens = MyLexer.tokens
    symbols = SymbolTable()
    code = None
        
    
    # program_all ---------------------------------------------------
    @_('procedures main',)
    def program_all(self, p):
        self.code = CodeGenerator(p.procedures, p.main, self.symbols)
        return self.code

    # procedures ----------------------------------------------------
    @_('procedures PROCEDURE proc_head IS declarations IN commands END',
       'procedures PROCEDURE proc_head IS IN commands END',
       '')
    def procedures(self, p):
        if len(p) == 8:
            for declaration in p.declarations:
                self.symbols.add_variable(str(p.proc_head + "_" + declaration))
        return ['PROCEDURES']

    # main ----------------------------------------------------------
    @_('PROGRAM IS declarations IN commands END',
       'PROGRAM IS IN commands END')
    def main(self, p):
        if len(p) == 6:
            for declaration in p.declarations:
                self.symbols.add_variable(declaration)
        return p.commands

    # commands ------------------------------------------------------
    @_('commands command')
    def commands(self, p):
        return p[0] + [p[1]]

    @_('command')
    def commands(self, p):
        return [p[0]]

    # command -------------------------------------------------------
    @_('IF condition THEN commands ENDIF',
       'IF condition THEN commands ELSE commands ENDIF',
       'WHILE condition DO commands ENDWHILE',
       'REPEAT commands UNTIL condition',
       'proc_call')
    def command(self, p):
        pass

    @_('WRITE value')
    def command(self, p):
        return 'write', p.value

    @_('READ identifier')
    def command(self, p):
        return 'read', p.identifier
    
    @_('identifier ASS expression')
    def command(self, p):
        return 'assign', p.identifier, p.expression

    # proc_head -----------------------------------------------------
    @_('PIDENTIFIER LPAREN args_decl RPAREN')
    def proc_head(self, p):
        return p.PIDENTIFIER

    # proc_call -----------------------------------------------------
    @_('PIDENTIFIER LPAREN args RPAREN')
    def proc_call(self, p):
        #self.result.append('PROC_CALL')
        pass

    # declarations --------------------------------------------------
    @_('declarations COMA PIDENTIFIER',
       'PIDENTIFIER')
    def declarations(self, p):
        if len(p) == 3:
            return p.declarations + p.PIDENTIFIER
        else:
            return p.PIDENTIFIER
        

    @_('declarations COMA PIDENTIFIER LBRACK NUM RBRACK',
       'PIDENTIFIER LBRACK NUM RBRACK')
    def declarations(self, p):
        if len(p) == 3:
            return p.declarations + p.PIDENTIFIER
        else:
            return p.PIDENTIFIER

    # args_decl -----------------------------------------------------
    @_('args_decl COMA PIDENTIFIER',
       'args_decl COMA T PIDENTIFIER',
       'PIDENTIFIER',
       'T PIDENTIFIER')
    def args_decl(self, p):
        #self.result.append('ARGS_DECL')
        pass

    # args ----------------------------------------------------------
    @_('args COMA PIDENTIFIER',
       'PIDENTIFIER')
    def args(self, p):
        #self.result.append('ARGS')
        pass

    # expression ----------------------------------------------------
    @_('value ADD value',
       'value SUB value',
       'value MUL value',
       'value DIV value',
       'value MOD value')
    def expression(self, p):
        #self.result.append('EXPRESSION ' + p[0] + ' ' + p[1] + ' ' + p[2])
        pass

    @_('value')
    def expression(self, p):
        return p.value

    # condition -----------------------------------------------------
    @_('value EQ value',
       'value NEQ value',
       'value GT value',
       'value LT value',
       'value GEQ value',
       'value LEQ value')
    def condition(self, p):
        #self.result.append('CONDITION ' + p[0] + ' ' + p[1] + ' ' + p[2])
        pass

    # value ---------------------------------------------------------
    @_('NUM',
       'identifier')
    def value(self, p):
        return p[0]

    # identifier ----------------------------------------------------
    @_('PIDENTIFIER')
    def identifier(self, p):
        return p.PIDENTIFIER

    @_('PIDENTIFIER LBRACK NUM RBRACK',
       'PIDENTIFIER LBRACK PIDENTIFIER RBRACK')
    def identifier(self, p):
        return p.PIDENTIFIER + p[2]

lexer = MyLexer()
parser = MyParser()
with open(sys.argv[1]) as in_f:
    text = in_f.read()

parser.parse(lexer.tokenize(text))
code = parser.code
code.gen_code()
with open(sys.argv[2], 'w') as out_f:
    for line in code.code:
        print(line, file=out_f)