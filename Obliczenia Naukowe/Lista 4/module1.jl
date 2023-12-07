#Szymon Pestrowicz
#268496

module module1

using Plots

export ilorazyRoznicowe, warNewton, rysujNnfx, naturalna

function ilorazyRoznicowe(x::Vector{Float64}, f::Vector{Float64})
    n = length(x);
    if(n != length(f))
      println("error")
      return;
    end
    fx = zeros(Float64, n)
    for i = 1 : n
      fx[i] = f[i];
    end
  
    for j = 1 : n
      for i = n : -1 : j+1
        fx[i] = (fx[i] - fx[i-1]) / (x[i] - x[i-j])
      end
    end
    return fx
  end

  function warNewton(x::Vector{Float64}, fx::Vector{Float64}, t::Float64)
    n = length(x)
    nt = fx[n];
    for i=n-1 : -1 : 1
      println(nt," * (",t," - ",x[i],") + ",fx[i])
      nt = nt * (t - x[i]) + fx[i];
    end
    println(nt)
    return nt;
  end

  function naturalna(x::Vector{Float64}, fx::Vector{Float64})
    n = length(x)
    a = zeros(Float64, n)
    poly = zeros(n+1, n+1)
    poly[1,1] = 1
    for j = 1:n-1
        poly[j+1, 1]=1
        poly[j+1, 2:j+1] = poly[j, 2:j+1]-x[j]*poly[j, 1:j]
    end
    for j=n : -1 : 1
      a[j] = fx[j]
      for i=1 : n-j
        a[j] = a[j] + fx[j+i]*poly[j+i, i+1]
      end
    end
    return a
  end

function rysujNnfx(f,a::Float64,b::Float64,n::Int)
  h = (b - a) / n;
  x = zeros(Float64, n + 1);
  y = zeros(Float64, n + 1);

  for i=1 : n + 1
    x[i] = a + (i-1) * h;
    y[i] = f(x[i]);
  end

  fx = ilorazyRoznicowe(x, y);
  closeness = 101;
  functionResults = zeros(Float64, closeness);
  interpResults = zeros(Float64, closeness);
  h1 = (b - a) / (closeness-1);
  for i=1 : closeness
    t = a + (i-1) * h1;
    functionResults[i] = f(t);
    interpResults[i] = warNewton(x, fx , t);
  end

  #p1 = plot(LinRange(a, b, closeness), functionResults, color ="blue", label = "functionResults")
  #p2 = plot!(LinRange(a, b, closeness), interpResults, color ="red", label="interpResults")
  #savefig("6b5.png")
end
end