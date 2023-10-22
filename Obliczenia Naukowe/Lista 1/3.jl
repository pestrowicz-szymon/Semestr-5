#Szymon Pestrowicz
#268496

#badanie przedzialu [1,2]
function firstpart()
    println("1          : ", bitstring(Float64(1.0)))
    println("1+2^(-52)  : ", bitstring(Float64(1+2.0^(-52))))
end
  
#badanie przedzialu [0.5, 1]
function secondpart()
    println("0.5        : ", bitstring(Float64(0.5)))
    println("0.5+2^(-53): ", bitstring(Float64(0.5+2.0^(-53))))
    println("0.5+2^(-52): ", bitstring(Float64(0.5+2.0^(-52))))
end
  
#badanie przedzialu [2,4]
function thirdpart()
    println("2          : ", bitstring(Float64(2.0)))
    println("2+2^(-51)  : ", bitstring(Float64(2+2.0^(-51))))
    println("2+2^(-52)  : ", bitstring(Float64(2+2.0^(-52))))
end

#badanie przedzialu [4,8]
function fourthpart()
    println("4          : ", bitstring(Float64(4.0)))
    println("4+2^(-50)  : ", bitstring(Float64(4+2.0^(-50))))
    println("4+2^(-51)  : ", bitstring(Float64(4+2.0^(-51))))
    println("4+2^(-52)  : ", bitstring(Float64(4+2.0^(-52))))
end
  
#wywolanie funkcji
firstpart()
println()
secondpart()
println()
thirdpart()
println()
fourthpart()
println()
println(bitstring(Float64(2.0-2.0^(-52))))