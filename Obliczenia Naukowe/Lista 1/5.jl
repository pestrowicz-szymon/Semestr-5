#Szymon Pestrowicz
#268496

x32 = Float32[2.718281828, -3.141592654, 1.414213562, 0.5772156649, 0.3010299957]
y32 = Float32[1486.2497, 878366.9879, -22.37492, 4773714.647, 0.000185049]
x64 = Float64[2.718281828, -3.141592654, 1.414213562, 0.5772156649, 0.3010299957]
y64 = Float64[1486.2497, 878366.9879, -22.37492, 4773714.647, 0.000185049]
n = 5

function a32()
    S = Float32(0.0)
    for i in 1:n
        S += x32[i]*y32[i]
    end
    println("Iloczyn skalarny w przód Float32:  ", S)
end

function a64()
    S = Float64(0.0)
    for i in 1:n
        S += x64[i]*y64[i]
    end
    println("Iloczyn skalarny w przód Float64:  ", S)
end

function b32()
    S = Float32(0.0)
    for i in 1:n
        S += x32[n-i+1]*y32[n-i+1]
    end
    println("Iloczyn skalarny w tył Float32:    ", S)
end

function b64()
    S = Float64(0.0)
    for i in 1:n
        S += x64[n-i+1]*y64[n-i+1]
    end
    println("Iloczyn skalarny w tył Float64:    ", S)
end

function cd32()
    vector32 = Float32[0.0, 0.0, 0.0, 0.0, 0.0]
    Sc = Float32(0.0)
    Sc1 = Float32(0.0)
    Sc2 = Float32(0.0)
    Sd1 = Float32(0.0)
    Sd2 = Float32(0.0)
    Sd = Float32(0.0)
    for i in 1:n
        vector32[i] = x32[i]*y32[i]
    end
    vector32 = sort(vector32, rev=true)

    for i in 1:3
        Sc1 += vector32[i]
    end
    for i in 0:1
        Sc2 += vector32[5-i]
    end
    Sc = Sc1 + Sc2

    for i in 1:3
        Sd1 += vector32[5 - i - 1]
    end
    for i in 4:5
        Sd2 += vector32[i]
    end
    Sd = Sd1 + Sd2

    println("Iloczyn skalarny malejaco FLoat32: ", Sc)
    println("Iloczyn skalarny rosnaco FLoat32:  ", Sd)
end

function cd64()
    vector64 = Float64[0.0, 0.0, 0.0, 0.0, 0.0]
    Sc = Float64(0.0)
    Sc1 = Float64(0.0)
    Sc2 = Float64(0.0)
    Sd1 = Float64(0.0)
    Sd2 = Float64(0.0)
    Sd = Float64(0.0)
    for i in 1:n
        vector64[i] = x64[i]*y64[i]
    end
    vector64 = sort(vector64, rev=true)

    for i in 1:3
        Sc1 += vector64[i]
    end
    for i in 0:1
        Sc2 += vector64[5-i]
    end
    Sc = Sc1 + Sc2

    for i in 1:3
        Sd1 += vector64[5 - i - 1]
    end
    for i in 4:5
        Sd2 += vector64[i]
    end
    Sd = Sd1 + Sd2

    println("Iloczyn skalarny malejaco FLoat64: ", Sc)
    println("Iloczyn skalarny rosnaco FLoat64:  ", Sd)
end

a32()
b32()
cd32()
a64()
b64()
cd64()