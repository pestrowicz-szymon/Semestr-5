from sly import Parser

from lexer import MyLexer
#from generator import CodeGenerator, Command

class MyParser(Parser):
    tokens = MyLexer.tokens # get tokens from lexer
    start = 'program_all'

    # set which operations are more important
    precedence = (
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIV', 'MOD')
    )

    # program_all
    @_('procedures main')
    def program_all(self, t):
        return 

    