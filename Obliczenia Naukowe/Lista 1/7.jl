#Szymon Pestrowicz
#268496

function f(x)
    return sin(x) + cos(3x)
end

function derivative(x, h)
    return (f(x+h) - f(x))/h
end

function realderivative(x)
    return cos(x) - 3 * sin(3x)
end

function error(x, y)
    return abs(x-y)
end

function main()
    h = Float64(1.0)
    for i in 0:54
        println("h = 2^-", i, " f'(1): ", derivative(Float64(1.0), h), " error: ", error(derivative(Float64(1.0), h), realderivative(Float64(1.0))))
        h = h/2
    end
end

println("real f'(1): ", realderivative(Float64(1.0)))
main()