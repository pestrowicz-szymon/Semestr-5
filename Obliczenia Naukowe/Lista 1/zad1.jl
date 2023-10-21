function macheps()
    x = Float16(1.0)
    xhelp = Float16(1.0)
    y = Float32(1.0)
    yhelp = Float32(1.0)
    z = Float64(1.0)
    zhelp = Float64(1.0)
  
    while(Float16(1.0 + x) > Float16(1.0))
      xhelp = x
      x = Float16(x/2)
    end
  
    while(Float32(1.0 + y) > Float32(1.0))
      yhelp= y
      y = Float32(y/2)
    end
  
    while(Float64(1.0 + z) > Float64(1.0))
      zhelp = z
      z = Float64(z/2)
    end
    println("macheps float16: ", xhelp)
    println("eps(float16): ", eps(Float16))
    println("macheps float32: ", yhelp)
    println("eps(float32): ", eps(Float32))
    println("macheps float64: ", zhelp)
    println("eps(float64): ", eps(Float64))
  end