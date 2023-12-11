#Szymon Pestrowicz
#268496
include("C:\\Users\\szymo\\Desktop\\Semestr-5\\Obliczenia Naukowe\\Lista 4\\module1.jl")
import .module1

#wynik powinien wynosić: [1.0,2.0,-0.375,0.175] (przykład z wykładu)
#println("ilorazy roznicowe: ", module1.ilorazyRoznicowe([-1.0, 0.0, 1.0, 2.0], [-1.0, 0.0, -1.0, 2.0]))

#wynik powinien wynosić: 1
#println("wartosc wielomianu: ", module1.warNewton([3.0, 1.0, 5.0, 6.0], module1.ilorazyRoznicowe([3.0, 1.0, 5.0, 6.0], [1.0, -3.0, 2.0, 4.0]) , 3.0))

#wynik powinien wynosić: [-8.75, 7.525, -1.95, 0.175]
println("naturalna: ", module1.naturalna([-1.0, 0.0, 1.0, 2.0], module1.ilorazyRoznicowe([-1.0, 0.0, 1.0, 2.0], [-1.0, 0.0, -1.0, 2.0] )))

# powinien zostać wkonany wykres funkcji |x|
# module1.rysujNnfx(x->abs(x), -1.0, 1.0, 5)