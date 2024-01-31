import sys

G_extended = [[1, 1, 0, 1, 0, 0, 0, 1],[0, 1, 1, 0, 1, 0, 0, 1],[0, 0, 1, 1, 0, 1, 0, 1],[0, 0, 0, 1, 1, 0, 1, 1]]
inputfile = sys.argv[1]
outputfile = sys.argv[2]
input = []
output = []
with open(inputfile, "rb+") as f:
    inp = f.read(1)
    while inp:
        inp=ord(inp)
        input.append(inp)
        inp=f.read(1)
    print(input)
    for i in range(len(input)):
        indicator = 0b10000000
        bits = [0,0,0,0,0,0,0,0]
        first = [0,0,0,0,0,0,0,0]
        second = [0,0,0,0,0,0,0,0]
        for j in range(8):
            bits[j] = 1 if input[i] & indicator else 0
            indicator = indicator >> 1
            #print(bits[j])
        for j in range(8):
            first[j] = 0
            second[j] = 0
            for k in range(4):
                first[j] ^= (G_extended[k][j] & bits[k])
                second[j] ^= (G_extended[k][j] & bits[k+4])

        #print(first)
        #print(second)
        output.append(first[7] + first[6]*2 + first[5]*4 + first[4]*8 + first[3]*16 + first[2]*32 + first[1]*64 + first[0]*128)
        output.append(second[7] + second[6]*2 + second[5]*4 + second[4]*8 + second[3]*16 + second[2]*32 + second[1]*64 + second[0]*128)

    with open(outputfile,"wb+") as out:
        for number in output:
            out.write(number.to_bytes(1, byteorder='big'))

