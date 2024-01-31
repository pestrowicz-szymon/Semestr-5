from sys import argv
from bitstring import ConstBitStream as bs, ReadError
from functools import reduce

def calc_bit_value(positions, bits):
    return reduce(lambda a, b: a+b, map(int, [bits[i] for i in positions])) % 2


def get_code(bits):

    b1 = calc_bit_value([0, 1, 3], bits)
    b2 = calc_bit_value([0, 2, 3], bits)
    b3 = calc_bit_value([1, 2, 3], bits)
    b4 = calc_bit_value([x for x in range(7)], [b1, b2, int(bits[0]), b3] + list(map(int, bits[1:])))

    return ''.join(map(str, [b1, b2, bits[0], b3, bits[1:], b4]))

input_f = argv[1]
output_f = argv[2]

b = bs(filename=input_f)
bitSequence = []
try:
    while True:
        bitSequence.append(b.read("uint:1"))
except ReadError:
    pass

bits = "".join(map(str, bitSequence))

print('input read')

i = 0
code = ''

while i < len(bits):
    code += get_code(bits[i:i+4])
    i += 4
    if i % 100000 == 0:
        print(i, len(bits))

print('encoded')

new_bytes = [code[i: i + 8] for i in range(0, len(code), 8)]
bytes_ = bytearray()

for i in new_bytes:
    bytes_.append(int(i, 2))

with open(output_f, "wb") as f:
    print('saving')
    f.write(bytes(bytes_))