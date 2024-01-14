from sly import Lexer, Parser
import sys

class MyLexer(Lexer):
    tokens = {
        'SZYM', 'KAS', 'NUM', 'PIDENTIFIER'
    }

    ignore = ' \t'
    ignore_comment = r'\#(.*?(\\\n)*)+\n'
    ignore_newline = r'\n+'

    SZYM = r'szym'
    KAS = r'kas'

    NUM = r'\d+'
    PIDENTIFIER = r'[_a-z]+'

class MyParser(Parser):
    tokens = MyLexer.tokens
    def __init__(self):
        self.result = ""

    #@_('SZYM')
    #def expression(self, p):
    #    self.result += 'S'

    #@_('KAS')
    #def expression(self, p):
    #    self.result += 'K'

    #@_('expression expression')
    #def expression(self, p):
    #    pass
        
    @_('symbol')
    def expression(self, p):
        pass

    @_('expression symbol')
    def expression(self, p):
        pass

    @_('SZYM')
    def symbol(self, p):
        self.result += 'S'

    @_('KAS')
    def symbol(self, p):
        self.result += 'K'

    @_('NUM')
    def symbol(self, p):
        self.result += 'NUM'

    @_('PIDENTIFIER')
    def symbol(self, p):
        self.result += p[0]
    
    
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
    print(result, file=out_f)