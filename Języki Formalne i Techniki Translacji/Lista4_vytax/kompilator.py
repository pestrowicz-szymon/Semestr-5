import sys
from lexer import MyLexer
from parser import MyParser
from generator import Generator

if len(sys.argv) != 3:
    print('Usage: python3 kompilator.py <input.imp> <output.mr>')
    exit(1)

path_in = sys.argv[1]
path_out = sys.argv[2]

lexer = MyLexer()
parser = MyParser()
generator = Generator()

with open(path_in) as file:
    input_text = file.read()
    tokens = lexer.tokenize(input_text)
    parser_result = parser.parse(tokens)
    codes = generator.compile_all(parser_result)

with open(path_out, "w") as file:
    for code in codes:
        file.write(str(code))
        file.write('\n')

print(f'Saved to {path_out}')