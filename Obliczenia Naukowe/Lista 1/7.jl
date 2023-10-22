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
    h = 1
    for i in 0:54
        println("h = 2^-", i, "f'(1): ", derivative(1, h), " error: ", error(derivative(1, h), realderivative(1)))
        h = h/2
    end
end

println("real f'(1): ", realderivative(1))
main()