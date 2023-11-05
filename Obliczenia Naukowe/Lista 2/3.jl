#Szymon Pestrowicz
#268496

using LinearAlgebra

function hilb(n::Int)
    if n < 1
        error("size n should be >= 1")
    end
    return [1 / (i + j - 1) for i in 1:n, j in 1:n]
end

function matcond(n::Int, c::Float64)
    if n < 2
        error("size n should be > 1")
    end
    if c < 1.0
        error("condition number  c of a matrix  should be >= 1.0")
    end
    (U, S, V) = svd(rand(n, n))
    return U * diagm(0 => [LinRange(1.0, c, n);]) * V'
end

function checkHilb(n)
    A = hilb(n)
    exact_x = ones(n)
    b = A * exact_x
    x_gauss = A \ b
    x_inv = inv(A) * b

    println("$n & $(rank(A)) & $(cond(A)) & $(norm(x_gauss - exact_x)/norm(exact_x)) & $(norm(x_inv - exact_x)/norm(exact_x))\\\\ \\hline")
end

function checkRandom(n, c)
    A = matcond(n, c)
    exact_x = ones(n)
    b = A * exact_x

    x_gauss = A \ b
    x_inv = inv(A) * b

    println("$n & $(rank(A)) & $(cond(A)) & $(norm(x_gauss - exact_x)/norm(exact_x)) & $(norm(x_inv - exact_x)/norm(exact_x))\\\\ \\hline")
end

println("Hilbert:")

for i in 1:2:30
    checkHilb(i)
end

sizes = [5, 10, 20]
conds = [1.0, 10.0, 10^3, 10^7, 10^12, 10^16]

println("Random:")

for size in sizes
    for cond in conds
        checkRandom(size, cond)
    end
end