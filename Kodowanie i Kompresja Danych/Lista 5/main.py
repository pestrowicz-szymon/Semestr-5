import sys
import numpy as np
from PIL import Image

def read_tga(filename):
    with open(filename, "br") as f:
        header = list(map(int, f.read(18))) # naglowek
        width = header[13]*256+header[12] # szerokosc obrazka
        height = header[15]*256+header[14] # wysokosc obrazka
        # tablica reprezentujaca pojedyncze pixele
        image_array = [[Pixel(0,0,0) for _ in range(width+2)] for _ in range(height+2)]
        # zczytywanie poszczególnych wartości pixeli i wstawianie ich w odpowiednie miejsca
        for row in range(height):
            for col in range(width):
                image_array[row+1][col+1] = Pixel(*(list(map(int, f.read(3)))[::-1]))
        # odwracamy kolejność pikseli i zwracamy taki obraz
        return image_array[::-1]
    
class Pixel:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def __add__(self, other):
        return Pixel(
            (self.r + other.r), 
            (self.g + other.g), 
            (self.b + other.b)
            )
    
    def __sub__(self, other):
        return Pixel(
            (self.r - other.r),
            (self.g - other.g), 
            (self.b - other.b)
        )

    def __floordiv__(self, n):
        return Pixel(
            self.r // 2,
            self.g // 2,
            self.b // 2
            )

    def __mod__(self, n):
        return Pixel(
            self.r % n,
            self.g % n,
            self.b % n
        )

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str((self.r, self.g, self.b))
    
def quantize(image, rBit, gBit, bBit):
    redLvl = 2 ** rBit
    greenLvl = 2 ** gBit
    blueLvl = 2 ** bBit

    if redLvl != 1:
        redTable = np.linspace(0, 255, redLvl, dtype=np.uint8)
    else:
        redTable = np.linspace(127, 128, redLvl, dtype=np.uint8)
    if greenLvl != 1:
        greenTable = np.linspace(0, 255, greenLvl, dtype=np.uint8)
    else:
        greenTable = np.linspace(127, 128, greenLvl, dtype=np.uint8)
    if blueLvl != 1:
        blueTable = np.linspace(0, 255, blueLvl, dtype=np.uint8)
    else:
        blueTable = np.linspace(127, 128, blueLvl, dtype=np.uint8)

    newImage = np.zeros_like(image, dtype=np.uint8)

    newImage[:, :, 0] = redTable[np.digitize(image[:, :, 0], redTable) - 1].astype(np.uint8)
    newImage[:, :, 1] = greenTable[np.digitize(image[:, :, 1], greenTable) - 1].astype(np.uint8)
    newImage[:, :, 2] = blueTable[np.digitize(image[:, :, 2], blueTable) - 1].astype(np.uint8)

    return newImage


def main():
    if len(sys.argv) != 6:
        print("Usage: ./kwantyzacja.py <input_file> <output_file> <bits_red> <bits_green> <bits_blue>")
        sys.exit(1)

    filenameIn = sys.argv[1]
    filenameOut = sys.argv[2]
    rBit = int(sys.argv[3])
    gBit = int(sys.argv[4])
    bBit = int(sys.argv[5])

    image = np.array(Image.open(filenameIn))

    quantized_image = quantize(image, rBit, gBit, bBit)

    Image.fromarray(quantized_image).save(filenameOut)


if __name__ == "__main__":
    main()