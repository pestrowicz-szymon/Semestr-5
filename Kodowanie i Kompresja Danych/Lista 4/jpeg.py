from math import log2
import sys

#   12-13 bajty - szerokosc obrazka
#   14-15 bajty - wysokosc obrazka

# zczytywanie pliku zgodnie ze standardem fga
# 18 bajtowy naglowek i 26 bajtowa stopka
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
                image_array[row+1][col+1] = Pixel(*(list(map(int, f.read(3)))))
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


def predictW(bit_map):
    prediction = [[None for _ in range(len(bit_map[0])-2)] for _ in range(len(bit_map)-2)]
    for y, row in enumerate(bit_map[1:-1],1):
        for x, pixel in enumerate(row[1:-1], 1):
            prediction[y-1][x-1] = (pixel - bit_map[y][x-1]) % 256
    return prediction


def predictN(bit_map):
    prediction = [[None for _ in range(len(bit_map[0])-2)] for _ in range(len(bit_map)-2)]
    for y, row in enumerate(bit_map[1:-1], 1):
        for x, pixel in enumerate(row[1:-1], 1):
            prediction[y-1][x-1] = (pixel - bit_map[y-1][x]) % 256
    return prediction


def predictNW(bit_map):
    prediction = [[None for _ in range(len(bit_map[0])-2)] for _ in range(len(bit_map)-2)]
    for y, row in enumerate(bit_map[1:-1], 1):
        for x, pixel in enumerate(row[1:-1], 1):
            prediction[y-1][x-1] = (pixel - bit_map[y-1][x-1]) % 256
    return prediction

# N + W - NW
def predictNW1(bit_map):
    prediction = [[None for _ in range(len(bit_map[0])-2)] for _ in range(len(bit_map)-2)]
    for y, row in enumerate(bit_map[1:-1], 1):
        for x, pixel in enumerate(row[1:-1], 1):
            N = bit_map[y-1][x]
            W = bit_map[y][x-1]
            NW = bit_map[y-1][x-1]
            prediction[y-1][x-1] = (pixel - (N + W - NW)) % 256
    return prediction

# N + (W - NW)/2
def predictNW2(bit_map):
    prediction = [[None for _ in range(len(bit_map[0])-2)] for _ in range(len(bit_map)-2)]
    for y, row in enumerate(bit_map[1:-1], 1):
        for x, pixel in enumerate(row[1:-1], 1):
            N = bit_map[y-1][x]
            W = bit_map[y][x-1]
            NW = bit_map[y-1][x-1]
            prediction[y-1][x-1] = (pixel - (N + (W - NW) // 2)) % 256
    
    return prediction

# W + (N - NW)/2
def predictNW3(bit_map):
    prediction = [[None for _ in range(len(bit_map[0])-2)] for _ in range(len(bit_map)-2)]
    for y, row in enumerate(bit_map[1:-1], 1):
        for x, pixel in enumerate(row[1:-1], 1):
            N = bit_map[y-1][x]
            W = bit_map[y][x-1]
            NW = bit_map[y-1][x-1]
            prediction[y-1][x-1] = (pixel - (W + (N - NW) // 2)) % 256
    
    return prediction

# (N+W)/2
def predictNW4(bit_map):
    prediction = [[None for _ in range(len(bit_map[0])-2)] for _ in range(len(bit_map)-2)]
    for y, row in enumerate(bit_map[1:-1], 1):
        for x, pixel in enumerate(row[1:-1], 1):
            N = bit_map[y-1][x]
            W = bit_map[y][x-1]
            prediction[y-1][x-1] = (pixel - (N + W) // 2 ) % 256
    return prediction

def predict_newer(bit_map):
    prediction = [[None for _ in range(len(bit_map[0])-2)] for _ in range(len(bit_map)-2)]
    for y, row in enumerate(bit_map[1:-1], 1):
        for x, pixel in enumerate(row[1:-1], 1):
            N = bit_map[y-1][x]
            W = bit_map[y][x-1]
            NW = bit_map[y-1][x-1]
            
            #tworzymy piksel z minimalnych i maksymalnych wartosci polnocnego i zachodniego
            minNW = Pixel(min(N.r, W.r), min(N.g, W.g), min(N.b, W.b))
            maxNW = Pixel(max(N.r, W.r), max(N.g, W.g), max(N.b, W.b))

            #opisane na slajdzie 4 z wykładu 6, jeżeli NW jest maksymalne albo minimalne
            #to bierzemy środkową wartość, wpp wyliaczymi W+N-NW
            r = minNW.r if NW.r >= maxNW.r else maxNW.r if NW.r <= minNW.r else N.r + W.r - NW.r
            g = minNW.g if NW.g >= maxNW.g else maxNW.g if NW.g <= minNW.g else N.g + W.g - NW.g
            b = minNW.b if NW.b >= maxNW.b else maxNW.b if NW.b <= minNW.b else N.b + W.b - NW.b
            prediction[y-1][x-1] = (pixel - Pixel(r,g,b)) % 256
    return prediction

#lista funkcji i ich nazw
types_desc = {
    predictW: "X̂ = W",
    predictN: "X̂ = N",
    predictNW: "X̂ = NW",
    predictNW1: "X̂ = N + W - NW",
    predictNW2: "X̂ = N + (W - NW)/2",
    predictNW3: "X̂ = W + (N - NW)/2",
    predictNW4: "X̂ = (N + W)/2",
    predict_newer: "new standard"
}

# funkcja obliczajaca entropie
def entropy(data_set):
    quantity = {i:0 for i in range(256)}
    for el in data_set:
        quantity[el] += 1       
    entropy = 0
    for el in range(256):
        if quantity[el] != 0:
            probability = quantity[el]/len(data_set)
            entropy -= probability*log2(probability)
    return entropy

#rozbijamy tablice pikseli 2d na ich liste jednowymiarowa
def bitmap_to_pixel_list(list_list):
    new_list = []
    for el in list_list:
        for ee in el:
            new_list.append(ee)
    return new_list

#rozbijamy tablice pikseli 2d na liste liczb, czyli przykladowo
#[(0,0,255)(0,1,254)(1,1,253)]
# rozbijemy na
#[0,0,255,0,1,254,1,1,253]
def bitmap_to_list(list_list):
    new_list = []
    for el in list_list:
        for ee in el:
            new_list.append(ee.r)
            new_list.append(ee.g)
            new_list.append(ee.b)
    return new_list

# funkcje zwracajace wartosci liczbowe tylko poszczegolnych kolorow
def get_green(bitmap_list):
    return [x.g for x in bitmap_list]

def get_blue(bitmap_list):
    return [x.b for x in bitmap_list]

def get_red(bitmap_list):
    return [x.r for x in bitmap_list]

def main():
    filename = sys.argv[1] 
    x = read_tga(filename)
    e_min = (8, None)
    er_min = (8, None)
    eg_min = (8, None)
    eb_min = (8, None)
    # x2 to kopia x ale bez jednopikselowej czarnej obramowki na zewnatrz
    x2 = [[x[i][j] for j in range(1,len(x[0])-1)] for i in range(1,len(x)-1)]
    # obliczamy entropie na liscie pikseli
    print(f"Input file: {filename}\n    entropy={entropy(bitmap_to_list(x2))}")
    # obliczamy entropie na liscie czerwonych wartosci
    print(f"    red_entropy={entropy(get_red(bitmap_to_pixel_list(x2)))}")
    # obliczamy entropie na liscie zielonych wartosci
    print(f"    green_entropy={entropy(get_green(bitmap_to_pixel_list(x2)))}")
    # obliczamy entropie na liscie niebieskich wartosci
    print(f"    blue_entropy={entropy(get_blue(bitmap_to_pixel_list(x2)))}\n")

    # typee - 'wskaznik' na funkcje ktorej wykorzystamy do liczenia
    # desc - opis 'graficzny' co liczmy
    for typee, desc in types_desc.items():
        # w y zapisujemy wyniki poszczegolnych predykcji
        y = typee(x)
        # a nastepnie w e1, er, eg, eb wyniki entropii tych predykcji
        e1 = entropy(bitmap_to_list(y))
        er = entropy(get_red(bitmap_to_pixel_list(y)))
        eg = entropy(get_green(bitmap_to_pixel_list(y)))
        eb = entropy(get_blue(bitmap_to_pixel_list(y)))

        # jezeli wartosci sa lepsze niz najnizsze obecnie uzyskane to wpisujemy je w e_min
        if e1 < e_min[0]:
            e_min = (e1, desc)
        if er < er_min[0]:
            er_min = (er, desc)
        if eg < eg_min[0]:
            eg_min = (eg, desc)
        if eb < eb_min[0]:
            eb_min = (eb, desc)

        #wypisanie rezultatow
        print(f"For prediction: {desc}")
        print(f"    entropy={e1}")
        print(f"    red_entropy={er}")
        print(f"    green_entropy={eg}")
        print(f"    blue_entropy={eb}")
        print()

    # wypisanie najlepszych rezultatow
    print(f"Best results:")
    print(f"    Total: {e_min[0]} for {e_min[1]}")
    print(f"    Red: {er_min[0]} for {er_min[1]}")
    print(f"    Green: {eg_min[0]} for {eg_min[1]}")
    print(f"    Blue: {eb_min[0]} for {eb_min[1]}")

        

if __name__ == "__main__":
    main()