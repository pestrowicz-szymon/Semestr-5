using Polynomials

wspolczynniki=[1, -210.0, 20615.0,-1256850.0, 53327946.0,-1672280820.0, 40171771630.0, -756111184500.0, 
    11310276995381.0, -135585182899530.0, 1307535010540395.0, -10142299865511450.0,
    63030812099294896.0,     -311333643161390640.0, 1206647803780373360.0, -3599979517947607200.0,
    8037811822645051776.0,      -12870931245150988800.0, 13803759753640704000.0, 
    -8752948036761600000.0, 2432902008176640000.0]

postac_naturalna = Polynomial(reverse(wspolczynniki))
#println("Wielomian P(x): ", postac_naturalna)

z_naturalne = roots(postac_naturalna)
#println(z_naturalne)

for k in 1:20
    println("|P(z", k, ")|: ", abs(postac_naturalna(z_naturalne[k])))
    println("|z", k, " - ", k, "|: ", abs(z_naturalne[k]-k))
    println()
end

println()
println("--------------------------------------------------------------------------------------")
println()

wspolczynniki2=[1, -210.0-2^-23, 20615.0,-1256850.0, 53327946.0,-1672280820.0, 40171771630.0, -756111184500.0, 
    11310276995381.0, -135585182899530.0, 1307535010540395.0, -10142299865511450.0,
    63030812099294896.0,     -311333643161390640.0, 1206647803780373360.0, -3599979517947607200.0,
    8037811822645051776.0,      -12870931245150988800.0, 13803759753640704000.0, 
    -8752948036761600000.0, 2432902008176640000.0]

postac_naturalna_b = Polynomial(reverse(wspolczynniki2))
#println("Wielomian P(x): ", postac_naturalna_b)

z_naturalne_b = roots(postac_naturalna_b)
#println(z_naturalne_b)

for k in 1:20
    println("|P(z", k, ")|: ", abs(postac_naturalna(z_naturalne_b[k])))
    println("|z", k, " - ", k, "|: ", abs(z_naturalne_b[k]-k))
    println()
end

#function wilkinson(x)
#    return  (x - 20)(x - 19)(x - 18)(x - 17)(x - 16)(x - 15)(x - 14)(x - 13)(x - 12)(x - 11)(x - 10)(x - 9)(x - 8)(x - 7)(x - 6)(x - 5)(x - 4)(x - 3)(x - 2)(x - 1)
#end
#wilres = roots(wilkinson(x))

