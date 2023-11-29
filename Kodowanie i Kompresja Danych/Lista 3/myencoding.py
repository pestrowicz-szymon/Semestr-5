import os
import math
from collections import defaultdict
from typing import List, Tuple

class Converter:
    def convert_file_to_byte_array(self, file_name):
        with open(file_name, 'rb') as file:
            byte_array = bytearray(file.read())
        return byte_array

    def get_frequency(self, byte_array):
        frequency = defaultdict(int)
        total_bytes = len(byte_array)

        for byte in byte_array:
            frequency[byte] += 1

        return {key: value / total_bytes for key, value in frequency.items()}

    def calculate_entropy1(self, frequency_map):
        entropy = -sum(prob * (0 if prob == 0 else math.log2(prob)) for prob in frequency_map.values())
        return entropy

    def calculate_entropy2(self, frequency_map):
        entropy = -sum(prob * (0 if prob == 0 else math.log2(prob)) for prob in frequency_map.values())
        return entropy


class Tuple:
    def __init__(self, first, second):
        self.first = first
        self.second = second


class Encoding_LZ77:
    def __init__(self):
        self.converter = Converter()
        self.k = 255
        self.n = 256
        self.dictionary_buffer = ""
        self.encoding_buffer = ""
        self.big_buffer = ""
        self.encoded_text = []

    def encoding(self, text_to_encoding, file_name):
        self.init_buffers(text_to_encoding)

        while len(self.encoding_buffer) != 0:
            encoded_tuple = self.one_step_of_encoding()
            self.encoded_text.append(encoded_tuple)

        self.get_values_describing_the_compression(text_to_encoding, file_name)
        return self.encoded_text

    def one_step_of_encoding(self):
        dictionary = self.dictionary_buffer
        our_pattern = self.encoding_buffer

        tuple_to_check = self.rabin_karp_search_all(our_pattern, dictionary)

        if isinstance(tuple_to_check.second, str):  # (0, letter_code)
            self.update_buffers(1)
        else:  # (i, j)
            c = tuple_to_check.second
            self.update_buffers(c)

        return tuple_to_check

    def init_buffers(self, text_to_encoding):
        self.dictionary_buffer += text_to_encoding[0] * max(0, self.k)

        for i in range(min(256, len(text_to_encoding) - 1)):
            self.encoding_buffer += text_to_encoding[i + 1]

        self.big_buffer += self.dictionary_buffer
        self.big_buffer += self.encoding_buffer
        if self.n + 1 < len(text_to_encoding):
            self.big_buffer += text_to_encoding[self.n + 1:]

        self.encoded_text.append(Tuple(0, text_to_encoding[0]))

    def update_buffers(self, j):
        self.dictionary_buffer = self.big_buffer[j:j + self.k]

        if j + self.k + self.n < len(self.big_buffer):
            self.encoding_buffer = self.big_buffer[j + self.k:j + self.k + self.n]
        else:
            self.encoding_buffer = self.big_buffer[j + self.k:]

        self.big_buffer = self.big_buffer[j:]

    def get_values_describing_the_compression(self, text_to_encoding, file_name):
        print("Wartości opisujące kompresję:")

        # długość kodowanego pliku
        length_of_text_to_encoding = len(text_to_encoding)
        print("długość kodowanego pliku:", length_of_text_to_encoding)

        # długość uzyskanego kodu
        length_of_code = len(self.encoded_text)
        print("długość uzyskanego kodu:", length_of_code)

        # stopień kompresji = dł przed skompresowaniem/dł po skompresowaniu
        print("stopień kompresji:", length_of_text_to_encoding / length_of_code)

        # entropia kodowanego tekstu
        byte_array = self.converter.convert_file_to_byte_array(file_name)
        frequency_map = self.converter.get_frequency(byte_array)
        text_entropy = self.converter.calculate_entropy1(frequency_map)
        print("entropia kodowanego tekstu:", text_entropy)

        # entropia uzyskanego kodu
        code_frequency_map = self.converter.get_frequency(self.encoded_text)
        code_entropy = self.converter.calculate_entropy2(code_frequency_map)
        print("entropia uzyskanego kodu:", code_entropy)


# Example usage:
# Create an instance of Encoding_LZ77
lz77_encoder = Encoding_LZ77()

# Replace 'textToEncoding' and 'fileName' with the actual values
text_to_encoding = "abcabcabc"
file_name = "example.txt"

# Call the encoding method
encoded_text = lz77_encoder.encoding(text_to_encoding, file_name)
