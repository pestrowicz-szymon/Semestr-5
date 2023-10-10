import math

# Funkcja obliczająca entropię na podstawie częstości symboli
def entropy(frequencies, total):
    result = 0.0
    for symbol, count in frequencies.items():
        probability = count / total
        result -= probability * math.log2(1/probability)
    return result

filename = input("Podaj nazwę pliku: ")

try:
    with open(filename, 'rb') as file:
        frequencies = {}  # Częstość występowania symboli
        conditional_frequencies = {}  # Częstość warunkowa
        prev_symbol = 0  # Symbol poprzedni

        while True:
            symbol = file.read(1)
            if not symbol:
                break

            symbol = symbol.decode('latin-1')
            frequencies[symbol] = frequencies.get(symbol, 0) + 1
            conditional_frequencies.setdefault(prev_symbol, {}).update({symbol: conditional_frequencies.get(prev_symbol, {}).get(symbol, 0) + 1})
            prev_symbol = symbol

        # Oblicz entropię
        total_symbols = len(frequencies)
        total_entropy = entropy(frequencies, total_symbols)

        # Oblicz entropię warunkową
        conditional_entropy = 0.0
        for prev_symbol, conditional_counts in conditional_frequencies.items():
            prev_symbol_count = frequencies[prev_symbol]
            conditional_entropy += (prev_symbol_count / total_symbols) * entropy(conditional_counts, prev_symbol_count)

        # Różnica między entropią a entropią warunkową
        difference = total_entropy - conditional_entropy

        print("Entropia:", total_entropy)
        print("Entropia warunkowa:", conditional_entropy)
        print("Różnica między nimi:", difference)

except FileNotFoundError:
    print("Nie udało się otworzyć pliku.")
except Exception as e:
    print("Wystąpił błąd:", e)