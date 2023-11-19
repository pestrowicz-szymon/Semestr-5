#Szymon Pestrowicz
#268496
include("C:\\Users\\szymo\\Desktop\\Semestr 5\\Obliczenia Naukowe\\Lista 3\\module1.jl")
import .module1

println("x^2 - 9")
println("metoda bisekcji:  ",module1.mbisekcji(x -> x^2 - 9, 1.5, 6.5, 5.0e-6,5.0e-6))
println("metoda stycznych: ",module1.mstycznych(x -> x^2 - 9, x -> 2*x, 1.5, 5.0e-6,5.0e-6, 50))
println("metoda siecznych: ",module1.msiecznych(x -> x^2 - 9, 1.0, 2.0, 5.0e-6,5.0e-6, 50))

println("\nx^4 - 16")
println("metoda bisekcji:  ",module1.mbisekcji(x -> x^4 - 16, 1.5, 6.5, 5.0e-6,5.0e-6))
println("metoda stycznych: ",module1.mstycznych(x -> x^4 - 16, x -> 4*(x^3), 1.5, 5.0e-6,5.0e-6, 50))
println("metoda siecznych: ",module1.msiecznych(x -> x^4 - 16, 1.0, 1.5, 5.0e-6,5.0e-6, 50))