from sys import argv

class Pixel:
    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue

    def __add__(self, other):
        return Pixel(
            self.red + other.red, self.green + other.green, self.blue + other.blue
        )

    def __sub__(self, other):
        return Pixel(
            self.red - other.red, self.green - other.green, self.blue - other.blue
        )

    def __mul__(self, number):
        return Pixel(self.red * number, self.green * number, self.blue * number)

    def __div__(self, number):
        return Pixel(self.red / number, self.green / number, self.blue / number)

    def __floordiv__(self, number):
        return Pixel(self.red // number, self.green // number, self.blue // number)

    def __mod__(self, number):
        return Pixel(self.red % number, self.green % number, self.blue % number)
    
    def __str__(self):
        return f"{self.red}, {self.green}, {self.blue}"

    def uniform_quantization(self, step):
        r = int(self.red // step * step)
        g = int(self.green // step * step)
        b = int(self.blue // step * step)
        return Pixel(r, g, b)


class Bitmap:
    def __init__(self, bitmap, width, height):
        self.width = width
        self.height = height

        result = []
        row = []
        for i in range(width * height):
            row.append(
                Pixel(
                    blue=bitmap[i * 3], green=bitmap[i * 3 + 1], red=bitmap[i * 3 + 2]
                )
            )

            if width == len(row):
                result.insert(0, row)
                row = []
        self.bitmap = result

    def __getitem__(self, pos):
        x, y = pos
        ret_x, ret_y = x, y
        if x < 0:
            ret_x = 0
        elif x >= self.width:
            ret_x = self.width - 1

        if y < 0:
            ret_y = 0
        elif y >= self.height:
            ret_y = self.height - 1

        return self.bitmap[ret_y][ret_x]
    
def calc_y(bitmap, x, y):
    if x+y == 0:
        pix = bitmap[x, y]
        return pix
    else:
        pix = Pixel(0, 0, 0)
        pix += bitmap[x, y]
        pix += bitmap[x-1, y-1]
        pix = pix // 2
        #('pixel1: ', bitmap[x, y], 'pixel2: ', bitmap[x-1, y-1], 'avg: ', pix)
        return pix   

def calc_z(bitmap, x, y):
    if x+y == 0:
        pass
    else:
        pix = Pixel(0, 0, 0)
        pix += bitmap[2*x, 2*y]
        pix -= bitmap[(2*x)-1, (2*y)-1]
        pix = pix // 2
        #print('pixel1: ', bitmap[2*x, 2*y], 'pixel2: ', bitmap[(2*x)-1, (2*y)-1], 'avg: ', pix)
        return pix
    
def quantify_uniform(bitmap, k):
    step = 256 // (2 ** k)
    return [pixel.uniform_quantization(step) for pixel in bitmap]

def encode(bitmap, k):
    half_width = bitmap.width
    half_height = bitmap.height
    y = [
        calc_y(bitmap, x, y)
        for y in range(half_height)
        for x in range(half_width)
    ]
    z = [
        calc_z(bitmap, x, y)
        for y in range(half_height)
        for x in range(half_width)
    ]
    quantified_y = quantify_uniform(y, k)
    quantified_z = quantify_uniform(z, k)



def main():
    if len(argv) == 3:
        with open(argv[1], "rb") as f:
            #read tga file
            tga = f.read()
            header = tga[:18]
            footer = tga[len(tga) - 26 :]
            width = tga[13] * 256 + tga[12]
            height = tga[15] * 256 + tga[14]
        
        #create bitmap from 'important' part of file
        #bitmap = Bitmap(tga[18 : len(tga) - 26], width, height) #normalnie
        bitmap = Bitmap(tga[18 : len(tga)], width, height) #example0

        k = argv[2]

        encoded = encode(bitmap, int(k))


    else:
        print('Usage: python main.py <input_file> <k_parameter>')

        


if __name__ == "__main__":
    main()