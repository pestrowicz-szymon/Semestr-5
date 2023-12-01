#Szymon Pestrowicz
#268496
include("C:\\Users\\szymo\\Desktop\\Semestr-5\\Obliczenia Naukowe\\Lista 3\\module1.jl")
import .module1

println("2x^2 - 4x")
println("metoda bisekcji:  ",module1.mbisekcji(x -> 2x^2 - 4x, -0.5, 0.5, 5.0e-6,5.0e-6))
println("metoda bisekcji:  ",module1.mbisekcji(x -> 2x^2 - 4x, 1.5, 2.5, 5.0e-6,5.0e-6))
println()
println("metoda stycznych: ",module1.mstycznych(x -> 2x^2 - 4x, x -> 4*x - 4, 0.5, 5.0e-6,5.0e-6, 50))
println("metoda stycznych: ",module1.mstycznych(x -> 2x^2 - 4x, x -> 4*x - 4, 1.5, 5.0e-6,5.0e-6, 50))
println()
println("metoda siecznych: ",module1.msiecznych(x -> 2x^2 - 4x, -0.5, 0.5, 5.0e-6,5.0e-6, 50))
println("metoda siecznych: ",module1.msiecznych(x -> 2x^2 - 4x, 1.5, 2.5, 5.0e-6,5.0e-6, 50))