#Szymon Pestrowicz
#268496

module module1

export mbisekcji, mstycznych, msiecznych

  function mbisekcji(f, a::Float64, b::Float64, delta::Float64, epsilon::Float64)
    u = f(a)
    v = f(b)
    e = b - a
  
    if sign(u) == sign(v)
      return 'x', 'x', 'x', 1
    end

    k=1
    while true
      e = e/2
      c = a+e
      w = f(c)

      if abs(b-a) <= delta && abs(w) <= epsilon
        return c, w, k, 0
      end

      if sign(w) != sign(u)
        b=c
        v=w
      else
        a=c
        u=w
      end

      k=k+1
    end
  end

  function mstycznych(f, pf, x0::Float64, delta::Float64, epsilon::Float64, maxit::Int)
    v = f(x0)

    if abs(v) < epsilon
      return x0, v, 0, 0
    end

    for k=1:maxit
      if abs(pf(x0)) < eps(Float64)
        return x1, v, k, 2
      end

      x1 = x0 - v/pf(x0)
      v = f(x1)

      if abs(x1-x0) < delta || abs(v) < epsilon
        return  x1, v, k, 0
      end

      x0 = x1
    end

    return x1, v, maxit, 1 
  end

  function msiecznych(f, x0::Float64, x1::Float64, delta::Float64, epsilon::Float64, maxit::Int)
    fx0 = f(x0)
    fx1 = f(x1)

    for k=1:maxit

      if abs(fx0) > abs(fx1)
        temp = x0
        x0 = x1
        x1 = temp
        temp = fx0
        fx0 = fx1
        fx1 = temp
      end

      s = (x1-x0)/(fx1-fx0)
      x1 = x0
      fx1 = fx0
      x0 = x0-fx0*s
      fx0 = f(x0)

      if abs(x1-x0) < delta || abs(fx0) < epsilon
        return x0, fx0, k, 0
      end

    end
    return x0, fx0, maxit, 1
  end

end