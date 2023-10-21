def build_prefix_table(pattern):
    m = len(pattern)
    prefix_table = [0] * m
    j = 0

    for i in range(1, m):
        while j > 0 and pattern[i] != pattern[j]:
            j = prefix_table[j - 1]

        if pattern[i] == pattern[j]:
            j += 1
        prefix_table[i] = j

    return prefix_table

def kmp_search(text, pattern):
    n = len(text)
    m = len(pattern)
    prefix_table = build_prefix_table(pattern)
    j = 0
    matches = []

    for i in range(n):
        while j > 0 and text[i] != pattern[j]:
            j = prefix_table[j - 1]

        if text[i] == pattern[j]:
            j += 1

        if j == m:
            matches.append(i - m + 1)
            j = prefix_table[j - 1]

    return matches

# Przykład użycia
text = "ababcababcababc"
pattern = "ababc"
matches = kmp_search(text, pattern)
print("Indeksy znalezionych dopasowań:", matches)