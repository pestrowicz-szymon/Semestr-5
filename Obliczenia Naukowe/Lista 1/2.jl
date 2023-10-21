#Szymon Pestrowicz
#268496

println("Kahan Float16: ", Float16(3) * (Float16(4) / Float16(3) - Float16(1)) - Float16(1))
println("eps(float16) : ", eps(Float16))
println("Kahan Float32: ", Float32(3) * (Float32(4) / Float32(3) - Float32(1)) - Float32(1))
println("eps(float32) : ", eps(Float32))
println("Kahan Float64: ", Float64(3) * (Float64(4) / Float64(3) - Float64(1)) - Float64(1))
println("eps(float64) : ", eps(Float64))