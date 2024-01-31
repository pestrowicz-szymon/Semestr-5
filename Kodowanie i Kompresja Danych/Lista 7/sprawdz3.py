import sys

def main():
    first_file = sys.argv[1]
    second_file = sys.argv[2]

    first_input = []
    second_input = []
    different = 0
    
    with open(first_file,"rb+") as f:
        inp = f.read(1)
        while inp:
            inp=ord(inp)
            first_input.append(inp)
            inp=f.read(1)

    with open(second_file,"rb+") as f:
        inp = f.read(1)
        while inp:
            inp=ord(inp)
            second_input.append(inp)
            inp=f.read(1)

    print(len(first_input))
    print(len(second_input))

    for i in range(len(first_input)):
        indicator = 0b10000000
        first = [0,0,0,0,0,0,0,0]
        second = [0,0,0,0,0,0,0,0]

        for j in range(8):
            first[j] = 1 if first_input[i] & indicator else 0
            second[j] = 1 if second_input[i] & indicator else 0
            indicator = indicator >> 1
        for j in range(4):
            if(first[j] != second[j]):
                different += 1
                break
        for j in range(4,8):
            if(first[j] != second[j]):
                different += 1
                break
    print("Wynik: ",different)
if __name__=="__main__":
    main()