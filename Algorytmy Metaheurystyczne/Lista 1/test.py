import random
import math

original_length = 131
for i in range(2*original_length):
    if math.floor(i/original_length) == 0:
        print (i, (i+1)%original_length)
    else:
        print(i%original_length, (i+2)%original_length)