from sly import Lexer, Parser
from CodeGenerator import Command, CodeGenerator
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

    def __init__(self):
        self.codeGenerator = CodeGenerator()
    
    # program_all ---------------------------------------------------
    @_('procedures main',)
    def program_all(self, p):
        return self.codeGenerator.generate_code(Command.PROGRAM_HALT, (p.procedures, p.main))

    # procedures ----------------------------------------------------
    @_('procedures PROCEDURE proc_head IS declarations IN commands END',)
    def procedures(self, p):
        return self.codeGenerator.generate_code(Command.PROCEDURES_VAR, (p.procedures, p.proc_head, p.commands))

    @_('procedures PROCEDURE proc_head IS IN commands END',)
    def procedures(self, p):
        return self.codeGenerator.generate_code(Command.PROCEDURES, (p.procedures, p.proc_head, p.commands))
    
    @_('')
    def procedures(self, p):
        return []
    
    # main ----------------------------------------------------------
    @_('PROGRAM IS declarations IN commands END')
    def main(self, p):
        return self.codeGenerator.generate_code(Command.MAIN_VAR, (None, p.commands))
    
    @_('PROGRAM IS IN commands END')
    def main(self, p):
        return self.codeGenerator.generate_code(Command.MAIN_VAR, (p.declarations, p.commands))
    
    # commands ------------------------------------------------------
    @_('commands command')
    def commands(self, p):
        return self.codeGenerator.generate_code(Command.COMMANDS_COMMAND, (p.commands, p.command))
    
    @_('command')
    def commands(self, p):
        return self.codeGenerator.generate_code(Command.COMMANDS_COMMAND, p.command)
    
    #@TODO write separate functions for all 'command'


    @_('identifier ASS expression',
       'IF condition THEN commands ENDIF',
       'IF condition THEN commands ELSE commands ENDIF',
       'WHILE condition DO commands ENDWHILE',
       'REPEAT commands UNTIL condition',
       'proc_call',
       'READ identifier',
       'WRITE value')
    def command(self, p):
        return p[0]

    @_('PIDENTIFIER LPAREN args_decl RPAREN')
    def proc_head(self, p):
        return p.PIDENTIFIER

    @_('PIDENTIFIER LPAREN args RPAREN')
    def proc_call(self, p):
        #self.result.append('PROC_CALL')
        pass

    @_('declarations COMA PIDENTIFIER',
       'declarations COMA PIDENTIFIER LBRACK NUM RBRACK',
       'PIDENTIFIER',
       'PIDENTIFIER LBRACK NUM RBRACK')
    def declarations(self, p):
        return p[0]

    @_('args_decl COMA PIDENTIFIER',
       'args_decl COMA T PIDENTIFIER',
       'PIDENTIFIER',
       'T PIDENTIFIER')
    def args_decl(self, p):
        #self.result.append('ARGS_DECL')
        pass

    @_('args COMA PIDENTIFIER',
       'PIDENTIFIER')
    def args(self, p):
        #self.result.append('ARGS')
        pass

    @_('value',
       'value ADD value',
       'value SUB value',
       'value MUL value',
       'value DIV value',
       'value MOD value',
       'value ASS value') # maybe it shouldnt be there, idk
    def expression(self, p):
        #self.result.append('EXPRESSION ' + p[0] + ' ' + p[1] + ' ' + p[2])
        pass

    @_('value EQ value',
       'value NEQ value',
       'value GT value',
       'value LT value',
       'value GEQ value',
       'value LEQ value')
    def condition(self, p):
        #self.result.append('CONDITION ' + p[0] + ' ' + p[1] + ' ' + p[2])
        pass

    @_('NUM',
       'identifier')
    def value(self, p):
        #self.result.append('VALUE ' + p[0])
        #return p[0]
        pass

    @_('PIDENTIFIER',
       'PIDENTIFIER LBRACK NUM RBRACK',
       'PIDENTIFIER LBRACK PIDENTIFIER RBRACK')
    def identifier(self, p):
        #self.result.append('IDENTIFIER ' + ' '.join(p))
        #return ' '.join(p)
        pass

    
lexer = MyLexer()
parser = MyParser()
with open(sys.argv[1]) as in_f:
    text = in_f.read()

result = parser.parse(lexer.tokenize(text))
print(result)

with open(sys.argv[2], 'w') as out_f:
    #for line in code_gen.code:
        #print(line, file=out_f)
    for line in result:
        print(line + '\n', file=out_f)
    #print(result, file=out_f)