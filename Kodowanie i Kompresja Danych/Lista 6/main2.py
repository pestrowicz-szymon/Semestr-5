from sys import argv
import numpy as np

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
    
def calc_y(list):
    result_list = []
    for i in range(len(list)):
        if i%2 == 0:
            result_list.append((list[i]+list[i+1])//2)
    result_list = calc_differences(result_list)
    return result_list
    

def calc_differences(list):
    result_list = []
    for i in range(len(list)):
        if i==0:
            result_list.append(list[i])
        else:
            result_list.append(list[i]-list[i-1])
    return result_list

def undo_differences(list):
    result_list = []
    for i in range(len(list)):
        if i==0:
            result_list.append(list[i])
        else:
            result_list.append(result_list[i-1]+list[i])
    return result_list

def calc_z(list, k):
    #in_list = quantify_uniform(list, k)
    result_list = []
    for i in range(len(list)):
        if i%2 == 0:
            result_list.append((list[i+1]-list[i])//2)
    #for i in range(len(list)):
    #    if i%2 == 0:
            #print(list[i], '|', in_list[i], '|', result_list[i//2])
    #    else:
            #print(list[i], '|', in_list[i])
    result_list = quantify_uniform(result_list, k)
    return result_list

def quantify_uniform(list, k):
    result_list = []
    quantify_level = 2**int(k)
    linspace = np.linspace(0, 255, quantify_level+1, dtype=np.uint16)
    for pixel in list:
        #print('original', pixel)
        newRed = linspace[np.digitize(abs(pixel.red), linspace, True)].astype(np.int32)
        newGreen = linspace[np.digitize(abs(pixel.green), linspace, True)].astype(np.int32)
        newBlue = linspace[np.digitize(abs(pixel.blue), linspace, True)].astype(np.int32)
        if pixel.red < 0:
            newRed = -newRed
        if pixel.green < 0:
            newGreen = -newGreen
        if pixel.blue < 0:
            newBlue = -newBlue
        newPixel = Pixel(newRed, newGreen, newBlue)
        #print('new', newPixel)
        result_list.append(newPixel)
    return result_list

def przypisz_wartosc(liczba, przedzialy):
    negative = liczba < 0
    if negative:
        liczba = -liczba
    for i in range(len(przedzialy)-1):
        if przedzialy[i] <= liczba <= przedzialy[i+1]:
            #print(liczba)
            if negative:
                return 0 - przedzialy[i]
            else:
                return przedzialy[i]
        else:
            #print(liczba)
            pass


def calc_x(y, z):
    if len(y) != len(z):
        print('ERROR len(y) != len(z)')
    result_list = []
    for i in range(len(y)):
        result_list.append(y[i]-z[i])
        result_list.append(y[i]+z[i])
    return result_list



def assign_to_space(linspace, value):
    for i in range(len(linspace)-1):
        if linspace[i] <= value <= linspace[i+1]:
            return i
        #else:
            #print(value)

def encode(list, k):
    y = calc_y(list)
    z = calc_z(list, k)
    return y, z

def decode(y, z):
    y_non_diff = undo_differences(y)
    x = calc_x(y_non_diff, z)
    for pix in x:
        pix.red = 0 if pix.red < 0 else pix.red
        pix.green = 0 if pix.green < 0 else pix.green
        pix.blue = 0 if pix.blue < 0 else pix.blue

        pix.red = 255 if pix.red > 255 else pix.red
        pix.green = 255 if pix.green > 255 else pix.green
        pix.blue = 255 if pix.blue > 255 else pix.blue
    return x

def convert_bitmap_to_pixel_list(bitmap, k):
    result = []
    for y in reversed(range(bitmap.height)):
        for x in range(bitmap.width):
            result.append(bitmap[x, y])
    return result

def convert_pixel_list_to_array(bitmap):
    payload = []
    for pixel in bitmap:
        payload += [pixel.blue, pixel.green, pixel.red]
    return payload

def d(a, b):
    return (a - b) ** 2

def mse(original, new):
    return (1 / len(original)) * sum([d(a, b) for a, b in zip(original, new)])

def tests(bitmap, new):
    original = [
        bitmap[x, y]
        for y in reversed(range(bitmap.height))
        for x in range(bitmap.width)
    ]
    original_array = []
    for pixel in original:
        original_array += [pixel.blue, pixel.green, pixel.red]

    original_red = [pixel.red for pixel in original]
    original_green = [pixel.green for pixel in original]
    original_blue = [pixel.blue for pixel in original]

    new_array = []
    for i in range(len(new) // 3):
        new_array += [new[i*3+0], new[i*3+1], new[i*3+2]]

    new_red = []
    for i in range(len(new) // 3):
        new_red += [new[i*3+2]]

    new_green = []
    for i in range(len(new) // 3):
        new_green += [new[i*3+1]]

    new_blue = []
    for i in range(len(new) // 3):
        new_blue += [new[i*3+0]]

    mserr = mse(original_array, new_array)
    mserr_red = mse(original_red, new_red)
    mserr_green = mse(original_green, new_green)
    mserr_blue = mse(original_blue, new_blue)   
    return mserr, mserr_red, mserr_green, mserr_blue

def signal_to_noise():
    #suma kwadratow oryginalow przez mse
    pass


def main():
    if len(argv) == 3:
        with open(argv[1], "rb") as f:
            tga = f.read()
            header = tga[:18]
            footer = tga[len(tga) - 26 :]
            width = tga[13] * 256 + tga[12]
            height = tga[15] * 256 + tga[14]
            #print('width and height', width, height)
        
        bitmap = Bitmap(tga[18 : len(tga) - 26], width, height) #normalnie
        #bitmap = Bitmap(tga[18 : len(tga)], width, height) #example0

        k = argv[2]

        pixel_list = convert_bitmap_to_pixel_list(bitmap, k)

        y, z = encode(pixel_list, k)

        x = decode(y, z)

        result = bytes(convert_pixel_list_to_array(x))

        #hope = bytes(convert_pixel_list_to_array(hope))

        with open(f'output_{argv[1]}', "wb") as f:
                f.write(header + result + footer)

        start_mse, start_mser, start_mseg, start_mseb= tests(bitmap, result)
        print('MSE', start_mse)
        print('MSE(red)', start_mser)
        print('MSE(green)', start_mseg)
        print('MSE(blue)', start_mseb)



    else:
        print('Usage: python main.py <input_file> <k_parameter>')

        


if __name__ == "__main__":
    main()