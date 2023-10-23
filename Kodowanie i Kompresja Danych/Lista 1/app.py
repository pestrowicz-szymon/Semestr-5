import math
import sys


def func(filename):
    with open(filename, 'rb') as file:
        #ba = bytearray(file.read())
        #print(len(ba))
        #for i in range(100):
        #    print(ba[i])
        symbolsFrequency = {}
        conditionalFrequency = {}
        numOfSymbols = 0
        previousSymbol = b'\x00'
        conditionalFrequency[previousSymbol] = {}

        while True:
            symbol = file.read(1)
            if not symbol:
                break

            numOfSymbols += 1

            if previousSymbol not in conditionalFrequency:
                conditionalFrequency[previousSymbol] = {}

            if symbol in conditionalFrequency[previousSymbol]:
                conditionalFrequency[previousSymbol][symbol] += 1
            else:
                conditionalFrequency[previousSymbol][symbol] = 1

            previousSymbol = symbol

            if symbol in symbolsFrequency:
                symbolsFrequency[symbol] += 1
            else:
                symbolsFrequency[symbol] = 1

        print(numOfSymbols)
        entRes = entropy(symbolsFrequency, numOfSymbols)
        conditionalEntRes = conditionalEntropy(conditionalFrequency, symbolsFrequency, numOfSymbols)
        print(entRes)
        print(conditionalEntRes)
        print(abs(conditionalEntRes - entRes))


def entropy(freq, numOfSymbols):
    H = 0
    for i in freq:
        H -= freq[i]/numOfSymbols * math.log(freq[i]/numOfSymbols, 2)
    return H


def conditionalEntropy(conditionalFrequency, freq, numOfSymbols):
    H = 0
    for i in freq:
        H -= freq[i]/numOfSymbols * sum(conditionalFrequency[i][j]/freq[i] * math.log(conditionalFrequency[i][j]/freq[i], 2) for j in conditionalFrequency[i])
    return H


if __name__ == '__main__':
    filename = sys.argv[1]
    func(filename)