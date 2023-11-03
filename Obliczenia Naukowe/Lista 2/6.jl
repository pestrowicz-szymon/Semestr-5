using CSV

csv_file = open("wyniki.csv", "w")

CSV.write(csv_file)

function rec(x, c)
    return x^2.0 + c
end

function repeat(x, c, n)
    resString = "$n"
    for i in 1:40
        x = rec(x, c)
        resString *= ";$x"
    end
    resString *= "\n"
    write(csv_file, resString)
end

repeat(Float64(1), Float64(-2), Float64(1))
repeat(Float64(2), Float64(-2), Float64(2))
repeat(Float64(1.99999999999999), Float64(-2), Float64(3))
repeat(Float64(1), Float64(-1), Float64(4))
repeat(Float64(-1), Float64(-1), Float64(5))
repeat(Float64(0.75), Float64(-1), Float64(6))
repeat(Float64(0.25), Float64(-1), Float64(7))

close(csv_file)