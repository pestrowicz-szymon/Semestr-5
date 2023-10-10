#include <iostream>
#include <fstream>
#include <vector>
#include <map>
#include <cmath>

using namespace std;

// Funkcja obliczająca entropię na podstawie częstości symboli
double entropy(const map<char, int>& frequencies, int total) {
    double result = 0.0;
    for (const auto& pair : frequencies) {
        double probability = static_cast<double>(pair.second) / total;
        result -= probability * log2(probability);
    }
    return result;
}

int main() {
    string filename;
    cout << "Podaj nazwę pliku: ";
    cin >> filename;

    ifstream file(filename, ios::binary);
    if (!file.is_open()) {
        cerr << "Nie udało się otworzyć pliku." << endl;
        return 1;
    }

    map<char, int> frequencies;  // Częstość występowania symboli
    map<char, map<char, int>> conditionalFrequencies;  // Częstość warunkowa

    char prevSymbol = 0; // Symbol poprzedni

    char symbol;
    while (file.get(symbol)) {
        frequencies[symbol]++;
        conditionalFrequencies[prevSymbol][symbol]++;
        prevSymbol = symbol;
    }

    // Oblicz entropię
    int totalSymbols = frequencies.size();
    double totalEntropy = entropy(frequencies, totalSymbols);
    
    // Oblicz entropię warunkową
    double conditionalEntropy = 0.0;
    for (const auto& pair : conditionalFrequencies) {
        int prevSymbolCount = frequencies[pair.first];
        conditionalEntropy += static_cast<double>(prevSymbolCount) / totalSymbols * entropy(pair.second, prevSymbolCount);
    }

    // Różnica między entropią a entropią warunkową
    double difference = totalEntropy - conditionalEntropy;

    cout << "Entropia: " << totalEntropy << endl;
    cout << "Entropia warunkowa: " << conditionalEntropy << endl;
    cout << "Różnica między nimi: " << difference << endl;

    file.close();
    return 0;
}
