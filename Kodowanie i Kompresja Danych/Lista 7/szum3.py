import sys
import random

def main():
    probability = float(sys.argv[1])
    filename = sys.argv[2]
    output = sys.argv[3]

    input = []
    result = []
    with open(filename,"rb+") as f:
        inp = f.read(1)
        while inp:
            inp=ord(inp)
            input.append(inp)
            inp=f.read(1)

    bits_flipped = 0

    for i in range(len(input)):
        indicator = 0b10000000
        bits = [0,0,0,0,0,0,0,0]
        for j in range(8):
            random_float = random.uniform(0,1)
            if (random_float >= probability):
                bits[j] = 1 if input[i] & indicator else 0
            else:
                bits_flipped += 1
                bits[j] = 0 if input[i] & indicator else 1
            indicator = indicator >> 1
        result.append(bits[7] + bits[6]*2 + bits[5]*4 + bits[4]*8 + bits[3]*16 + bits[2]*32 + bits[1]*64 + bits[0]*128)

    with open(output,"wb+") as out:
        for number in result:
            out.write(number.to_bytes(length=(8 + (number + (number < 0)).bit_length()) // 8, byteorder='big', signed=True))
    print("Flipped: ", bits_flipped)

if __name__=="__main__":
    main()