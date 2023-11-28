import sys
from myencoding import Encoding_LZ77
from mydecoding import Decoding_LZ77

def convert_file_to_string(file_name):
    with open(file_name, 'r') as file:
        text = file.read()
    return text

if __name__ == "__main__":
    encoding_lz77 = Encoding_LZ77()
    decoding_lz77 = Decoding_LZ77()

    # Zamiast args[0] używamy sys.argv[1], ponieważ sys.argv[0] to nazwa skryptu
    if len(sys.argv) < 2:
        print("Usage: python script.py <file_name>")
        sys.exit(1)

    file_name = sys.argv[1]
    text_to_encoding = convert_file_to_string(file_name)

    if len(text_to_encoding) <= 1:
        raise ValueError("Text to encoding must be longer than 1!")

    encoded_text = encoding_lz77.encoding(text_to_encoding, file_name)

    # Możesz odkomentować poniższą linijkę, aby wyświetlić każdy Tuple
    # for tuple_item in encoded_text:
    #     print(tuple_item.first, tuple_item.second)

    decoding_lz77.decoding(encoded_text)
