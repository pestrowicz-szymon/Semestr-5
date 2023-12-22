import sys
import numpy as np
from PIL import Image
    
def quantize(image, Bit):
    currBestR = 9
    currBestG = 9
    currBestB = 9
    currBestImage = image
    currBestMse = float('inf')

    for r in range(Bit+1): 
        for g in range(Bit+1-r):
            for b in range(Bit+1-r-g):
                if r+g+b == Bit:
                    print(r, g, b)
                    redLvl = 2 ** r
                    greenLvl = 2 ** g
                    blueLvl = 2 ** b

                    #if redLvl != 1:
                    redTable = np.linspace(0, 255, redLvl+1, dtype=np.uint8)
                    #else:
                    #    redTable = np.linspace(127, 128, redLvl+1, dtype=np.uint8)
                    #if greenLvl != 1:
                    greenTable = np.linspace(0, 255, greenLvl+1, dtype=np.uint8)
                    #else:
                    #    greenTable = np.linspace(127, 128, greenLvl, dtype=np.uint8)
                    #if blueLvl != 1:
                    blueTable = np.linspace(0, 255, blueLvl+1, dtype=np.uint8)
                    #else:
                    #    blueTable = np.linspace(127, 128, blueLvl, dtype=np.uint8)

                    newImage = np.zeros_like(image, dtype=np.uint8)

                    newImage[:, :, 0] = redTable[np.digitize(image[:, :, 0], redTable) - 1].astype(np.uint8)
                    newImage[:, :, 1] = greenTable[np.digitize(image[:, :, 1], greenTable) - 1].astype(np.uint8)
                    newImage[:, :, 2] = blueTable[np.digitize(image[:, :, 2], blueTable) - 1].astype(np.uint8)

                    newMse = calcMse(image, newImage)
                    
                    print("mse(r)=", calcMse(image[:, :, 0], newImage[:, :, 0]))
                    print("mse(g)=", calcMse(image[:, :, 1], newImage[:, :, 1]))
                    print("mse(b)=", calcMse(image[:, :, 2], newImage[:, :, 2]))
                    print("mse   =", newMse)

                    if newMse < currBestMse:
                        currBestImage = newImage
                        currBestR = r
                        currBestG = g
                        currBestB = b
        
    print("found rgb:", currBestR, currBestG, currBestB)
    return currBestImage

def calcMse(original, quantized):
    return np.mean((original - quantized) ** 2)

def main():
    if len(sys.argv) != 4:
        print("Usage: ./main2.py <input_file> <output_file> <bits>")
        sys.exit(4)

    print(sys.argv)

    filenameIn = sys.argv[1]
    filenameOut = sys.argv[2]
    Bit = int(sys.argv[3])

    image = np.array(Image.open(filenameIn))

    quantized_image = quantize(image, Bit)

    print("mse   =", calcMse(image, quantized_image))

    Image.fromarray(quantized_image).save(filenameOut)

        
if __name__ == "__main__":
    main()