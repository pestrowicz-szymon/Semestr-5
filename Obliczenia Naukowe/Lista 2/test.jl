using LinearAlgebra

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

#x = matcond(5, 10.0)
#println(x)
for i in 1:2:30
    println(i)
end