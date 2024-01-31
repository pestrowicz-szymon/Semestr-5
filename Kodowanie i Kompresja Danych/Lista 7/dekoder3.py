import sys

def main():

    parity_matrix = [[0,0,1,0,1,1,1],[0,1,0,1,1,1,0],[1,0,1,1,1,0,0]]

    err_id = {1:0,2:1,5:2,3:3,7:4,6:5,4:6}

    filename = sys.argv[1]
    output=sys.argv[2]
    input = []
    result = []
    with open(filename,"rb+") as f:
        inp = f.read(1)
        while inp:
            inp=ord(inp)
            input.append(inp)
            inp=f.read(1)
    two_err_counter = 0
    corrected_counter = 0
    prev_bits = [0,0,0,0,0,0,0,0]

    for i in range(len(input)):
        indicator = 0b10000000
        bits = [0,0,0,0,0,0,0,0]
        for j in range(8):
            bits[j] = 1 if input[i] & indicator else 0
            indicator = indicator >> 1
        error = False
        check_output = [0,0,0]
        for j in range(3):
            for k in range(7):
                check_output[j] ^= (parity_matrix[j][k] & bits[k])
            if (check_output[0] or check_output[1] or check_output[2]):
                error = True
            parity = True
            for j in range(8):
                parity ^= bits[j]
            if error:
                if parity:
                    two_err_counter += 1
                else:
                    id = err_id[check_output[2] + check_output[1]*2 + check_output[0]*4]
                    print(bits[id])
                    bits[id] = 0 if bits[id] else 1
                    corrected_counter += 1
        if i%2==0:
            for j in range(8):
                prev_bits[j] = bits[j]
        else:
            indicator = 0b10000000
            dec_bits= [prev_bits[0], prev_bits[0] ^ prev_bits[1], prev_bits[5], prev_bits[6], bits[0], bits[0] ^ bits[1], bits[5], bits[6]]
            dec_byte = 0
            for j in range(8):
                dec_byte += dec_bits[j] * indicator
                indicator = indicator >> 1
            result.append(dec_byte)
    with open(output,"wb+") as out:
        for number in result:
            out.write(number.to_bytes(length=(8 + (number + (number < 0)).bit_length()) // 8, byteorder='big', signed=True))

    print("Poprawiono: ",corrected_counter)
    print("Dwa błędy: ", two_err_counter)
    
if __name__=="__main__":
    main()