#Szymon Pestrowicz
#268496

#funkcja znajdujaca macheps dla float16, float32 i float64
function macheps()
    f16 = Float16(1.0)
    f16help= Float16(1.0)
    f32= Float32(1.0)
    f32help = Float32(1.0)
    f64 = Float64(1.0)
    f64help = Float64(1.0)

    while(Float16(1.0 + f16) > Float16(1.0))
        f16help = f16
        f16 = Float16(f16/2)
    end

    while(Float32(1.0 + f32) > Float32(1.0))
        f32help = f32
        f32 = Float32(f32/2)
    end

    while(Float64(1.0 + f64) > Float64(1.0))
        f64help = f64
        f64 = Float64(f64/2)
    end

    println("macheps f16:  ", f16help)
    println("eps(float16): ", eps(Float16))
    println("macheps f32:  ", f32help)
    println("eps(float32): ", eps(Float32))
    println("macheps f64:  ", f64help)
    println("eps(float64): ", eps(Float64))
end

#funkcja znajdujaca eta dla float16, float32 i float64
function eta()
    f16 = Float16(1.0)
    f16help= Float16(1.0)
    f32= Float32(1.0)
    f32help = Float32(1.0)
    f64 = Float64(1.0)
    f64help = Float64(1.0)

    while(f16 > Float16(0.0))
        f16help = f16
        f16 = Float16(f16/2)
    end

    while(f32 > Float32(0.0))
        f32help = f32
        f32 = Float32(f32/2)
    end

    while(f64 > Float64(0.0))
        f64help = f64
        f64 = Float64(f64/2)
    end

    println("eta f16           : ", f16help)
    println("nextfloat(float16): ", nextfloat(Float16(0.0)))
    println("eta f32           : ", f32help)
    println("nextfloat(float32): ", nextfloat(Float32(0.0)))
    println("eta f64           : ", f64help)
    println("nextfloat(float64): ", nextfloat(Float64(0.0)))
end

#funkcja znajdujaca max dla kazdego typu
function max()
    f16 = Float16(1.0)
    f32 = Float32(1.0)
    f64 = Float64(1.0)

    while !isinf(Float16(f16*2.0))
        f16 = Float16(f16*2.0)
    end
    f16 = Float16(f16*prevfloat(Float16(2.0)))

    while !isinf(Float32(f32*2.0))
        f32 = Float32(f32*2.0)
    end
    f32 = Float32(f32*prevfloat(Float32(2.0)))

    while !isinf(Float64(f64*2.0))
        f64 = Float64(f64*2.0)
    end
    f64 = Float64(f64*prevfloat(Float64(2.0)))

    println("MAX float 16     : ", f16)
    println("floatmax(Float16): ", floatmax(Float16))
    println("MAX float 32     : ", f32)
    println("floatmax(Float32): ", floatmax(Float32))
    println("MAX float 64     : ", f64)
    println("floatmax(Float64): ", floatmax(Float64))
end

macheps()
println()
eta()
println()
max()
println()
println("floatmin(Float32): ", floatmin(Float32))
println("floatmin(Float64): ", floatmin(Float64))