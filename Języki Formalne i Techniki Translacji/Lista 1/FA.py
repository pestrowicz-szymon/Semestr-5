import sys

if(len(sys.argv) < 3):
    sys.exit("Nie podano wymaganych argumentów (wzorca i nazwy pliku)")

def ComputeTransitionFunction(pattern, alphabet):
    m = len(pattern)
    for q in range(m+1):
        transitionTable[q] = {}
        for a in alphabet:
            k = min(m, q+1)
            while k > 0 and pattern[:k] != pattern[q - k + 1:q] + a:
                k-=1
            transitionTable[q][a] = k

def FiniteAutomationMatcher(text, transitionTable, pattern):
    n = len(text)
    q = 0
    matches = []
    for i in range(n):
        q = transitionTable[q][text[i]]
        if q == len(pattern):
            matches.append(i - len(pattern) + 1)
    return matches




pattern = sys.argv[1]
text = open(sys.argv[2], "r", encoding="utf-8").read()
print(text)
print(pattern)
transitionTable = {}
ComputeTransitionFunction(pattern, set(text))
matches = FiniteAutomationMatcher(text, transitionTable, pattern)
print(matches)







            