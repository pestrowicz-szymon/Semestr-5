weights = [[1, 0, 0], [1, 2, 3], [1, 15, -2]]

weights_sum = sum([sum(row) for row in weights])

print(weights_sum)
print()
for row in weights:
    print(sum(row))
print()
for row in weights:
    print(row)