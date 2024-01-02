#Szymon Pestrowicz 268496
include("./matrixgen.jl")
include("./blocksys.jl")
using LinearAlgebra
using SparseArrays
using .matrixgen
using .blocksys

function runDane(index::Int64)
    #create variables for output file name and size
    out = ""
    size = 0;
    #choose which data to use
    if index == 1
        matrixFile1 = open("./data/Dane16_1_1/A.txt")
        vectorFile1 = open("./data/Dane16_1_1/b.txt")
        matrixFile2 = open("./data/Dane16_1_1/A.txt")
        vectorFile2 = open("./data/Dane16_1_1/b.txt")
        out = "Dane16_1_1"
        size = 16
    elseif index == 2
        matrixFile1 = open("./data/Dane10000_1_1/A.txt")
        vectorFile1 = open("./data/Dane10000_1_1/b.txt")
        matrixFile2 = open("./data/Dane10000_1_1/A.txt")
        vectorFile2 = open("./data/Dane10000_1_1/b.txt")
        out = "Dane10000_1_1"
        size = 10000
    elseif index == 3
        matrixFile1 = open("./data/Dane50000_1_1/A.txt")
        vectorFile1 = open("./data/Dane50000_1_1/b.txt")
        matrixFile2= open("./data/Dane50000_1_1/A.txt")
        vectorFile2 = open("./data/Dane50000_1_1/b.txt")
        out = "Dane50000_1_1"
        size = 50000
    elseif index == 4
        matrixFile1 = open("./data/Dane100000_1_1/A.txt")
        vectorFile1 = open("./data/Dane100000_1_1/b.txt")
        matrixFile2 = open("./data/Dane100000_1_1/A.txt")
        vectorFile2 = open("./data/Dane100000_1_1/b.txt")
        out = "Dane100000_1_1"
        size = 100000
    else
        return 
    end
    
    #read A and b
    matrix1 = ReadMatrix(matrixFile1)
    vector1 = ReadVector(vectorFile1)

    #read A and b once again
    matrix2 = ReadMatrix(matrixFile2)
    vector2 = ReadVector(vectorFile2)

    #save result to solvedGauss, time to t and memory to m
    (solvedGaussWithPivots, t1, m1) = @timed GaussWithPivots(matrix1, vector1, size, 4)
    (solvedGauss, t2, m2) = @timed Gauss(matrix2, vector2, size, 4)
    
    x = ones(Float64, size)
    #calculate error of calculations
    err1 = norm(solvedGaussWithPivots - x)/norm(x)
    err2 = norm(solvedGauss - x)/norm(x)
    
    #print time, memory and error
    println("Gauss With Pivots ",t1, " ", m1, " ", err1)
    println("Gauss ", t2, " ", m2, " ", err2)

    #write results to files, f is shortcut for fileName
    open(string("OutGauss",out), "w") do f
        for i in solvedGauss
            println(f, i)
        end
    end

    open(string("OutGaussPivots",out), "w") do f
        for i in solvedGaussWithPivots
            println(f, i)
        end
    end

end

runDane(1)
runDane(2)
runDane(3)
runDane(4)