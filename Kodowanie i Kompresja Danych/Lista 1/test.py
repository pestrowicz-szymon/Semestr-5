import math
import sys


def func(filename):
    with open(filename, 'rb') as file:
        while True:
            symbol = file.read(1)
            print(symbol)

if __name__ == '__main__':
    filename = sys.argv[1]
    func(filename)