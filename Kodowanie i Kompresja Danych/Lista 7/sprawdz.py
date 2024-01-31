from sys import argv
from bitstring import ConstBitStream as bs, ReadError

input_f1 = argv[1]
input_f2 = argv[2]

b = bs(filename=input_f1)
bitSequence = []
try:
    while True:
        bitSequence.append(b.read("uint:1"))
except ReadError:
    pass

bits1 = "".join(map(str, bitSequence))


b = bs(filename=input_f2)
bitSequence = []
try:
    while True:
        bitSequence.append(b.read("uint:1"))
except ReadError:
    pass

bits2 = "".join(map(str, bitSequence))

diffs = 0
for x in range(4, len(bits1)+1, 4):
    if(bits1[x-4:x] != bits2[x-4:x]):
        diffs += 1

print(f'Znaleziono {diffs} różnice')