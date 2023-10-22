#Szymon Pestrowicz
#268496

function calc()
    x = nextfloat(Float64(1.0))
    while (Float64(x * Float64(1/x)) == Float64(1.0))
        x = nextfloat(Float64(x))
    end
    println("x: ", Float64(x), " 1/x: ", Float64(1/x), " x*1/x: ", Float64(x * Float64(1/x)))
end

function calc2()
    x = nextfloat(Float64(0.0))
    while (Float64(x * Float64(1/x)) == Float64(1.0))
        x = nextfloat(Float64(x))
    end
    println("x: ", Float64(x), " 1/x: ", Float64(1/x), " x*1/x: ", Float64(x * Float64(1/x)))
end

calc()
calc2()