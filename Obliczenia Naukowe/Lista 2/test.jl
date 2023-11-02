using Polynomials  # Importowanie pakietu Polynomials

# Współczynniki wielomianu
coefficients = [(-20:1:-16)...; (-15:1:-11)...; (-10:1:-6)...; (-5:1:-1)...]

# Tworzenie wielomianu
p = polynomial(coefficients)

# Wyświetlenie wielomianu
println(p)