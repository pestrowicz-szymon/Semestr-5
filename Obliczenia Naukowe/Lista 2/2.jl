using Plots 
using Calculus
using SymPy

f(x) = exp(x) * log(1 + exp(-x))

p = plot(f, -10, 50)
savefig(p, "plot.png")

x=symbols("x");
println(limit(f(x), x => oo))