#include <cstdio>
#include <string>
#include <cmath>

const int SIZE = 1234577;
std::string expression = "";
bool errorOccured = false;

int valueFromField(int64_t n) {
    int result = (int)(n % SIZE);
    if (result < 0)
        result += SIZE;
    return result;
}

int valueFromFieldForExp(int64_t n) {
    int result = (int)(n % (SIZE - 1));
    if (result < 0)
        result += SIZE - 1;
    return result;
}

void addNumber(int n) {
    expression += std::to_string(valueFromField(n)) + " ";
}

void addExpNumber(int n) {
    expression += std::to_string(valueFromFieldForExp(n)) + " ";
}

// Funkcja pomocnicza do obliczania największego wspólnego dzielnika
int gcd(int a, int b) {
    if (b == 0)
        return a;
    return gcd(b, a % b);
}

// Funkcja sprawdzająca, czy liczba n jest odwracalna modulo m
bool isReversible(int n, int m) {
    // Sprawdzenie, czy n i m są względnie pierwsze
    return gcd(n, m) == 1;
}

int inverse(int n) {
    int t = 0;
    int r = SIZE;
    int newt = 1;
    int newr = valueFromField(n);

    if(!isReversible(newr, SIZE)) {
        printf("%d is not reversible modulo %d\n", newr, SIZE);
        errorOccured = true;
        return 0;
    }

    while (newr != 0) {
        int quotient = r / newr;

        int curr = newt;
        newt = t - quotient * newt;
        t = curr;

        curr = newr;
        newr = r - quotient * newr;
        r = curr;
    }
    
    return valueFromField(t);
}

int add(int a, int b) {
    expression += "+ ";
    return valueFromField(a) + valueFromField(b);
}

int sub(int a, int b) {
    expression += "- ";
    return valueFromField(a) - valueFromField(b);
}

int mul(int a, int b) {
    expression += "* ";
    int64_t n1 = valueFromField(a);
    int64_t n2 = valueFromField(b);
    return valueFromField(a * b);
}

int divide(int a, int b) { 
    expression += "/ ";
    int64_t n1 = valueFromField(a);
    int64_t n2 = inverse(b);
    return n1 * n2;
}

int power(int a, int b) {
    expression += "^ ";
    int64_t base = valueFromField(a);
    int64_t exp = valueFromFieldForExp(b);
    int result = 1;

    while (exp > 0) {
        if (exp & 1)
            result = (result * base) % SIZE;
        base = (base * base) % SIZE;
        exp >>= 1;
    }

    return valueFromField(result);
}

void showResult(int n) {
    printf("%s\n", expression.c_str());
    printf("Result : %d\n", valueFromField(n));
    expression.clear();
}

void handleError() {
    fprintf(stderr, "Error\n");
    expression.clear();
}