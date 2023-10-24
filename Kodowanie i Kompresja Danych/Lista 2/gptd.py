import pickle

class Node:
    def __init__(self, char, frequency):
        self.char = char
        self.frequency = frequency
        self.left = None
        self.right = None

def decode_text(encoded_text, huffman_codes):
    # Funkcja do dekodowania zakodowanego tekstu
    decoded_text = ""
    current_code = ""
    for bit in encoded_text:
        current_code += bit
        for char, code in huffman_codes.items():
            if code == current_code:
                decoded_text += char
                current_code = ""
                break
    return decoded_text

def bytes_to_binary_string(bytes_data):
    # Przekształć bajty na ciąg bitów
    binary_string = ''.join(format(byte, '08b') for byte in bytes_data)
    return binary_string

def decode_file(input_file, output_file):
    # Odczytaj zakodowany plik
    with open(input_file, 'rb') as file:
        huffman_codes = pickle.load(file)
        encoded_bytes = file.read()

    # Krok 1: Przekształć zakodowany tekst z powrotem na ciąg bitów
    encoded_text = bytes_to_binary_string(encoded_bytes)

    # Krok 2: Dekoduj zakodowany tekst
    decoded_text = decode_text(encoded_text, huffman_codes)

    # Krok 3: Zapisz odkodowany tekst do pliku wyjściowego
    with open(output_file, 'w') as file:
        file.write(decoded_text)

if __name__ == "__main__":
    input_file = input("Podaj nazwę pliku zakodowanego: ")
    output_file = input("Podaj nazwę pliku wyjściowego: ")

    decode_file(input_file, output_file)
    print("Plik został zdekodowany i zapisany jako", output_file)
