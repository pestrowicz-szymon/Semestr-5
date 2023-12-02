class Tuple:
    def __init__(self, first, second):
        self.first = first
        self.second = second


class Decoding_LZ77:
    def __init__(self):
        self.k = 255
        self.n = 256
        self.dictionary_buffer = ""
        self.output_buffer = ""

    def decoding(self, encoded_text):
        self.init_buffers(encoded_text[0])

        for i in range(1, len(encoded_text)):
            self.one_step_of_decoding(encoded_text[i])

        self.write_decoded_text_to_file(self.output_buffer)

    def init_buffers(self, tuple_obj):
        first_letter = str(tuple_obj.second)
        self.dictionary_buffer += first_letter * max(0, self.k)
        self.output_buffer += first_letter

    def one_step_of_decoding(self, tuple_obj):
        if isinstance(tuple_obj.second, str):  # (0, letter_code)
            new_letters = tuple_obj.second

            # shift by 1 and add new letters
            self.dictionary_buffer = self.dicti
