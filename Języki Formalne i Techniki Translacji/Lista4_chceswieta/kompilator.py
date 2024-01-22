from my_lexer import MyLexer
from my_parser import MyParser
from code_generator import CodeGenerator
import sys
lexer = MyLexer()
parser = MyParser()
generator = CodeGenerator()
with open(sys.argv[1]) as in_f:
    text = in_f.read()
codes = generator.generate_executable(parser.parse(lexer.tokenize(text)))
with open(sys.argv[2], 'w') as out_f:
    for line in codes:
        print(str(line), file=out_f)