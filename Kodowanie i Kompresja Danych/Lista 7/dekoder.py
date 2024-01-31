from sys import argv
from bitstring import ConstBitStream as bs, ReadError
from functools import reduce

def get_code(bits):

    b1 = calc_bit_value([0, 1, 3], bits)
    b2 = calc_bit_value([0, 2, 3], bits)
    b3 = calc_bit_value([1, 2, 3], bits)
    b4 = calc_bit_value([x for x in range(7)], [
                        b1, b2, int(bits[0]), b3] + list(map(int, bits[1:])))
    return ''.join(map(str, [b1, b2, bits[0], b3, bits[1:], b4]))

def calc_bit_value(positions, bits):
    return reduce(lambda a, b: a+b, map(int, [bits[i] for i in positions])) % 2

def get_message(bits):
    for code in possible_codes:
        if reduce(lambda x, y: x+y, [1 if x != y else 0 for x, y in zip(bits, code)]) < 2:
            return bits[2] + bits[4:7], False
    return '0000', True


def decode(bits, possible_codes):

    def get_message(bits):
        for code in possible_codes:
            if reduce(lambda x, y: x+y, [1 if x != y else 0 for x, y in zip(bits, code)]) < 2:
                return bits[2] + bits[4:7], False
        return '0000', True

    i = 0
    errors = 0
    msg = ''
    while i < len(bits):
        code, error = get_message(bits[i:i+8])

        msg += code
        errors += 1 if error else 0
        i += 8

    return msg, errors

input_f = argv[1]
output_f = argv[2]

possible_codes = []
for x in range(16):
    possible_codes.append(get_code(bin(x)[2:].zfill(4)))

b = bs(filename=input_f)
bitSequence = []
try:
    while True:
        bitSequence.append(b.read("uint:1"))
except ReadError:
    pass

bits = "".join(map(str, bitSequence))

decoded, errors = decode(bits, possible_codes)

new_bytes = [decoded[i: i + 8] for i in range(0, len(decoded), 8)]

bytes_ = bytearray()

for i in new_bytes:
    bytes_.append(int(i, 2))

with open(output_f, "wb") as f:
    print('saving')
    f.write(bytes(bytes_))

print(f'W {errors}/{int(len(bits)/8)} przypadkach wystąpiły dwa błędy')