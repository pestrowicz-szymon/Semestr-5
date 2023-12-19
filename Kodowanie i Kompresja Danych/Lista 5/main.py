import sys
import numpy as np
from PIL import Image
    
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

def calcMse(original, quantized):
    return np.mean((original - quantized) ** 2)

def calcSnr(mse):
    #snr
    return (255 ** 2 / mse)
    # snr w dB
    # return 10 * np.log10(255 ** 2 / mse)

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

    print("mse   =", calcMse(image, quantized_image))
    print("mse(r)=", calcMse(image[:, :, 0], quantized_image[:, :, 0]))
    print("mse(g)=", calcMse(image[:, :, 1], quantized_image[:, :, 1]))
    print("mse(b)=", calcMse(image[:, :, 2], quantized_image[:, :, 2]))
    print("snr   =", calcSnr(calcMse(image, quantized_image)))
    print("snr(r)=", calcSnr(calcMse(image[:, :, 0], quantized_image[:, :, 0])))
    print("snr(g)=", calcSnr(calcMse(image[:, :, 1], quantized_image[:, :, 1])))
    print("snr(b)=", calcSnr(calcMse(image[:, :, 2], quantized_image[:, :, 2])))
    

    Image.fromarray(quantized_image).save(filenameOut)


if __name__ == "__main__":
    main()