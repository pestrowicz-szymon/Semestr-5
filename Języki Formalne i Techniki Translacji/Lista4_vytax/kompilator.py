import sys
from lexer import MyLexer
from parser import MyParser
from generator import Generator

if len(sys.argv) != 3:
    print('Sposób użycia: python3 kompilator.py <plik_wejściowy.imp> <plik_wyjściowy.mr>')
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

print('Kompilacja zakończona pomyślnie')