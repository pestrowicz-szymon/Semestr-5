#include <cstdio>
#include <string>
#include <cmath>

const int SIZE = 1234577;
std::string expression = "";

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

int inverse(int n) {
    int t = 0;
    int r = SIZE;
    int newt = 1;
    int newr = valueFromField(n);

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
    return valueFromField(valueFromField(a) + valueFromField(b));
}

int sub(int a, int b) {
    expression += "- ";
    return valueFromField(valueFromField(a) - valueFromField(b));
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
    return valueFromField(n1 * n2);
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