import heapq
import os
import pickle
import math
import sys
import struct
from bitstring import BitArray

class Node:
    def __init__(self, char, frequency):
        self.char = char
        self.frequency = frequency
        self.left = None
        self.right = None
    
    def __lt__(self, other):
        return self.frequency < other.frequency

''' 
def printNodes(node, val=''): 
  
    # huffman code for current node 
    newVal = val
  
    # if node is not an edge node 
    # then traverse inside it 
    if(node.left): 
        printNodes(node.left, newVal) 
    if(node.right): 
        printNodes(node.right, newVal) 
  
        # if node is edge node then 
        # display its huffman code 
    if(not node.left and not node.right): 
        print(f"{node.char} -> {newVal}") 
'''    
        
def build_huffman_tree(text):
    char_frequency = {}
    for symbol in text:
        if symbol in char_frequency:
            char_frequency[symbol] += 1
        else:
            char_frequency[symbol] = 1

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

    #printNodes(heap[0])
    
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
        #print(char, ": ", huffman_codes[char])
        encoded_text += huffman_codes[char]
    return encoded_text

def binary_string_to_bytes(binary_string):
    # Przekształć ciąg bitów na bajty
    binary_string = '0' * (8 - len(binary_string) % 8) + binary_string
    bytes_list = [int(binary_string[i:i+8], 2) for i in range(0, len(binary_string), 8)]
    return bytes(bytes_list)

def bitstring_to_bytes(s):
    return int(s, 2).to_bytes((len(s) + 7) // 8, byteorder='big')

def bitstring_to_bytes2(s):
    print("w funkcji: ", s)
    v = int(s, 2)
    print("v          ", s)
    b = bytearray()
    while v:
        print("wewnatrz while: ", v & 0xff)
        b.append(v & 0xff)
        v >>= 8
    print(b)
    return bytes(b[::-1])
        
def encode(input, output):
    with open(input, 'r', encoding='utf-8') as file:
        text = file.read()

    huffman_tree = build_huffman_tree(text)

    huffman_codes = {}
    generate_huffman_codes(huffman_tree, "", huffman_codes)

    print(huffman_codes)

    #print("huffman codes")
    #print(huffman_codes)

    encoded_text = encode_text(text, huffman_codes)

    #print("encoded text: ", encoded_text)

    with open(output, 'wb') as file:
        pickle.dump(huffman_codes, file)  # Zapisz kody do pliku
        #bytes_text = binary_string_to_bytes(encoded_text)
        #print("bytes text: ", bytes_text)
        reverted_encoded_text = encoded_text [::-1]
        #print(encoded_text)
        
        #print("encoded: ", encoded_text)
        #print("chat: ", binary_string_to_bytes(reverted_encoded_text))
        #print("stack: ", bitstring_to_bytes(reverted_encoded_text))
        binary_string = ''
        for byte in binary_string_to_bytes(reverted_encoded_text):
            #print(byte)
            binary_string += bin(byte)[2:].zfill(8)
        
        binary_string = binary_string [::-1]
        print(binary_string)

        print(bitstring_to_bytes2(encoded_text))

        #print(binary_string)

        

        #byts = bitstring_to_bytes(binary_string)
        #print(byts)
        
        #newFileByteArray = bytearray(binary_string)
        #print(newFileByteArray)
        #file.write(newFileByteArray)

        #c = BitArray(hex=binary_string_to_bytes(encoded_text))
        #c.bin
        #print("spowrotem: ", c)
        #file.write(bytes_text)
        #file.write(encoded_text)







def decode(input, output):
    with open(input, 'r', encoding='utf-8') as file:
        text = file.read()

if __name__ == '__main__':
    inputfile = sys.argv[2]
    outputfile = sys.argv[3]
    if sys.argv[1] == '--encode':
        encode(inputfile, outputfile)
    elif sys.argv[1] == '--decode':
        #print("decoding not implemented yet")
        decode(inputfile, outputfile)