import heapq
import os
import pickle

class Node:
    def __init__(self, char, frequency):
        self.char = char
        self.frequency = frequency
        self.left = None
        self.right = None
    
    def __lt__(self, other):
        return self.frequency < other.frequency

def build_huffman_tree(text):
    # Funkcja do budowy drzewa kodowania Huffmana
    char_frequency = {}
    
    # Liczenie częstotliwości wystąpień znaków w tekście
    for char in text:
        if char in char_frequency:
            char_frequency[char] += 1
        else:
            char_frequency[char] = 1
    
    # Tworzenie kolejki priorytetowej
    heap = [Node(char, freq) for char, freq in char_frequency.items()]
    heapq.heapify(heap)
    
    # Budowa drzewa Huffmana
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        parent = Node(None, left.frequency + right.frequency)
        parent.left = left
        parent.right = right
        heapq.heappush(heap, parent)
    
    return heap[0]  # Węzeł korzenia drzewa

def generate_huffman_codes(node, current_code, huffman_codes):
    # Funkcja do generowania kodów dla znaków na podstawie drzewa
    if node is None:
        return
    
    if node.char is not None:
        huffman_codes[node.char] = current_code
    generate_huffman_codes(node.left, current_code + '0', huffman_codes)
    generate_huffman_codes(node.right, current_code + '1', huffman_codes)

def encode_text(text, huffman_codes):
    # Funkcja do zakodowania tekstu za pomocą kodów Huffmana
    encoded_text = ""
    for char in text:
        encoded_text += huffman_codes[char]
    return encoded_text

def binary_string_to_bytes(binary_string):
    # Przekształć ciąg bitów na bajty
    binary_string = '0' * (8 - len(binary_string) % 8) + binary_string
    bytes_list = [int(binary_string[i:i+8], 2) for i in range(0, len(binary_string), 8)]
    return bytes(bytes_list)

def encode_file(input_file, output_file):
    # Odczytaj zawartość pliku wejściowego
    with open(input_file, 'r') as file:
        text = file.read()

    # Krok 1: Buduj drzewo kodowania Huffmana
    huffman_tree = build_huffman_tree(text)

    # Krok 2: Generuj kody dla znaków
    huffman_codes = {}
    generate_huffman_codes(huffman_tree, "", huffman_codes)

    # Krok 3: Zakoduj tekst
    encoded_text = encode_text(text, huffman_codes)

    # Krok 4: Zapisz zakodowany tekst do pliku wyjściowego
    with open(output_file, 'wb') as file:
        pickle.dump(huffman_codes, file)  # Zapisz kody do pliku
        bytes_text = binary_string_to_bytes(encoded_text)
        file.write(bytes_text)

if __name__ == "__main__":
    input_file = input("Podaj nazwę pliku wejściowego: ")
    output_file = input("Podaj nazwę pliku wyjściowego: ")

    encode_file(input_file, output_file)
    print("Plik został zakodowany i zapisany jako", output_file)
