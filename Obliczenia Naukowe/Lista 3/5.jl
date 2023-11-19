#Szymon Pestrowicz
#268496
include("C:\\Users\\szymo\\Desktop\\Semestr 5\\Obliczenia Naukowe\\Lista 3\\module1.jl")
import .module1

println("metoda bisekcji: [0.0, 1.0] x = ",module1.mbisekcji(x->(ℯ^x)-(3*x), 0.0, 1.0, 1.0e-4,1.0e-4))
println("metoda bisekcji: [1.0, 2.0] x = ",module1.mbisekcji(x->(ℯ^x)-(3*x), 1.0, 2.0, 1.0e-4,1.0e-4))