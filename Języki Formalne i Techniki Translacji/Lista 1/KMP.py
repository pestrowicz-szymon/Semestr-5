import sys

if(len(sys.argv) < 3):
    sys.exit("Nie podano wymaganych argumentów (wzorca i nazwy pliku)")

def ComputePrefixFunction(pattern):
    m = len(pattern)
    pi = [0] * m
    k = 0
    for q in range(2, m):
        while k > 0 and pattern[q] != pattern [k]:
            k = pi[k - 1]
        if pattern[k] == pattern[q]:
            k += 1
        pi[q] = k
    return pi

def KMPMatcher(text, pattern):
    n = len(text)
    m = len(pattern)
    pi = ComputePrefixFunction(pattern)
    q = 0
    matches = []
    for i in range(n):
        while q > 0 and text[i] != pattern[q]:
            q = pi[q-1]
        if text[i] == pattern[q]:
            q += 1
        if q == m:
            matches.append(i - m + 1)
            q = pi[q-1]
        return matches
    
pattern = sys.argv[1]
text = open(sys.argv[2], "r", encoding="utf-8").read()
matches = KMPMatcher(text, pattern)
print(matches)
