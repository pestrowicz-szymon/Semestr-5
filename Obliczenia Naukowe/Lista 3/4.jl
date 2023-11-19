#Szymon Pestrowicz
#268496
include("C:\\Users\\szymo\\Desktop\\Semestr 5\\Obliczenia Naukowe\\Lista 3\\module1.jl")
import .module1

println("sin(x) - (x/2)^2")
println("metoda bisekcji:  ",module1.mbisekcji(x -> sin(x) - ((1/2)*x)^2, 1.5, 2.0, 5.0e-6, 5.0e-6))
println("metoda stycznych: ",module1.mstycznych(x -> sin(x) - ((1/2)*x)^2, x -> cos(x) - x/2, 1.5, 5.0e-6, 5.0e-6, 50))
println("metoda siecznych: ",module1.msiecznych(x -> sin(x) - ((1/2)*x)^2, 1.0, 2.0, 5.0e-6, 5.0e-6, 50))