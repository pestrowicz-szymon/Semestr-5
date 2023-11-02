function iteration(pn, r)
    return pn + r*pn*(1-pn)
end

function forty(p0_1, r)
    x = p0_1
    for i in 1:40
        x = iteration(x, r)
    end
    return x
end

function tenthirty(p0_2, r)
    x = p0_2
    for i in 1:10
        x = iteration(x, r)
    end

    #println("x po 10 iteracjach: ", x)
    x = trunc(x, digits=3)
    #println("x po obcięciu: ", x)

    for i in 1:30
        x = iteration(x, r)
    end
    return x
end

p0_1 = Float32(0.01)
p0_2 = Float32(0.01)
r = Float32(3)

println("Float32: ")
println(forty(p0_1, r))
println(tenthirty(p0_2, r))

println()

p0_1_64 = Float64(0.01)
p0_2_64 = Float64(0.01)
r_64 = Float64(3)

println("Float64: ")
println(forty(p0_1_64, r_64))
println(tenthirty(p0_2_64, r_64))