#Szymon Pestrowicz
#268496

function f(x)
    return sqrt(x * x + 1) - 1
end

function g(x)
    return (x*x) / sqrt(x * x + 1) + 1
end

function main()
    k = Float64(1/8)
    for i in 1:10
        println("f(8^-", i, "): ",f(k))
        println("g(8^-", i, "): ",g(k))
        k *= 1/8
        println()
    end
end

main()