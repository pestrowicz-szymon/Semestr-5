from sys import argv
from bitstring import ConstBitStream as bs, ReadError
from random import random

probability = argv[1]
input_f = argv[2]
output_f = argv[3]

b = bs(filename=input_f)
bitSequence = []
try:
    while True:
        bitSequence.append(b.read("uint:1"))
except ReadError:
    pass

bits = "".join(map(str, bitSequence))

switched = ''.join([str(1 - int(bit)) if random() < float(probability) else bit for bit in bits])

new_bytes = [switched[i: i + 8] for i in range(0, len(switched), 8)]
bytes_ = bytearray()

for i in new_bytes:
    bytes_.append(int(i, 2))

with open(output_f, "wb") as f:
    f.write(bytes(bytes_))