import sys
from lexer import MyLexer
from parser import MyParser
from generator import Generator

#if len(sys.argv) != 3:
#    print('Sposób użycia: python3 kompilator.py <plik_wejściowy.imp> <plik_wyjściowy.mr>')
#    exit(1)

#path_in = sys.argv[1]
#path_out = sys.argv[2]
test_file = 'proc/example1'

path_in = sys.argv[1]
path_out = sys.argv[2]

lexer = MyLexer()
parser = MyParser()
generator = Generator()

with open(path_in) as file:
    input_text = file.read()
    tokens = lexer.tokenize(input_text)
    ast = parser.parse(tokens)
    print(ast)
    #exit(0)
    codes = generator.generate_all(ast)
    #for code in codes:
    #    print(code)
    #for tok in tokens:
    #    print('type=%r, value=%r' % (tok.type, tok.value))

with open(path_out, "w") as file:
    for code in codes:
        file.write(str(code))
        file.write('\n')

#print(f"Kompilacja zakończona pomyślnie")
