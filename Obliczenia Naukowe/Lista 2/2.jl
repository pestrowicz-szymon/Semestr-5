using Plots 

f(x) = exp(x) * log(1 + exp(-x))
p = plot(f, -10, 50)
savefig(p, "plot.png")