#Szymon Pestrowicz
#268496
include("C:\\Users\\szymo\\Desktop\\Semestr 5\\Obliczenia Naukowe\\Lista 3\\module1.jl")
import .module1

println("e^(x-1) - 1:")
println("metoda bisekcji:  ",module1.mbisekcji(x -> ℯ^(1-x) - 1, 0.0, 2.0, 1.0e-5, 1.0e-5))
println("metoda stycznych: ",module1.mstycznych(x -> ℯ^(1-x) - 1, x -> -ℯ^(1-x), 0.2, 1.0e-5, 1.0e-5, 50))
println("metoda siecznych: ",module1.msiecznych(x -> ℯ^(1-x) - 1, 0.5, 1.5, 1.0e-5, 1.0e-5, 50))

println("\nx*e^(-x):")
println("metoda bisekcji:  ",module1.mbisekcji(x -> x*ℯ^(-x), -1.0, 1.0, 1.0e-5, 1.0e-5))
println("metoda stycznych: ",module1.mstycznych(x -> x*ℯ^(-x), x -> (-ℯ^(-x))*(x-1), 0.5, 1.0e-5, 1.0e-5, 50))
println("metoda siecznych: ",module1.msiecznych(x -> x*ℯ^(-x), -1.0, 1.0, 1.0e-5, 1.0e-5, 50))

println("\nmetoda stycznych: ",module1.mstycznych(x -> ℯ^(1-x) - 1, x -> -ℯ^(1-x), 4.0, 1.0e-5, 1.0e-5, 50))
println("metoda stycznych: ",module1.mstycznych(x -> x*ℯ^(-x), x -> (-ℯ^(-x))*(x-1), 1.0, 1.0e-5, 1.0e-5, 50))