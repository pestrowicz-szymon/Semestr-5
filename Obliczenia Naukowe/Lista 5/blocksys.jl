#Szymon Pestrowicz 268496
module blocksys
    include("./matrixgen.jl")
    export ReadMatrix, ReadVector, Gauss, GaussWithPivots, runTest, calculateRightSide

    using  SparseArrays
    using .matrixgen
    using PyPlot

    function runTest(maxSize::Int64, step::Int64, blockSize::Int64, rep::Int64)
        sizeVector = []

        timeGaussVector = []
        memoryGaussVector = []

        timeGaussWithPivotsVector = []
        memoryGaussWithPivotsVector = []

        for size in step:step:maxSize
            timeGauss = 0.0
            memoryGauss = 0.0

            timeGaussWithPivots = 0.0
            memoryGaussWithPivots = 0.0

            for reps in 1:rep
                blockmat(size, blockSize, 1.0, "tmp.txt")
                tmp1 = open("tmp.txt")
                M1 = ReadMatrix(tmp1)
                b1 = calculateRightSide(M1, size, blockSize)

                tmp2 = open("tmp.txt")
                M2 = ReadMatrix(tmp2)
                b2 = calculateRightSide(M2, size, blockSize)

                (_, t, m) = @timed GaussWithPivots(M1, b1, size, blockSize)
                timeGaussWithPivots += t;
                memoryGaussWithPivots += m
                
                

                (_, t, m) = @timed Gauss(M2, b2, size, blockSize)
                timeGauss += t;
                memoryGauss += m

            end

            timeGauss /= rep
            memoryGauss /= rep

            timeGaussWithPivots /= rep
            memoryGaussWithPivots /= rep

            push!(sizeVector, size)

            push!(timeGaussVector, timeGauss)
            push!(memoryGaussVector, memoryGauss)

            push!(timeGaussWithPivotsVector, timeGaussWithPivots)
            push!(memoryGaussWithPivotsVector, memoryGaussWithPivots)

            println(size, ";", timeGauss, ";", memoryGauss, ";", timeGaussWithPivots, ";", memoryGaussWithPivots)
        end
        clf()
        plot(sizeVector, timeGaussVector, label="Gauss")
        plot(sizeVector, timeGaussWithPivotsVector, label="GaussWithPivots")
        grid(true)
        title("Time")
        legend(loc=2,borderaxespad=0)
        savefig("Time.png")
        
        
        clf()
        plot(sizeVector, memoryGaussVector, label="Gauss")
        plot(sizeVector, memoryGaussWithPivotsVector, label="GaussWithPivots")
        grid(true)
        title("Memory")
        legend(loc=2,borderaxespad=0)
        savefig("Memory.png")

    end

    function ReadMatrix(file::IOStream) :: SparseMatrixCSC{Float64, Int}
        columns = []
        rows = []
        values = []

        for line in Iterators.drop(eachline(file), 1)
            words = split(line)
            push!(rows, parse(Int, words[1]))
            push!(columns, parse(Int, words[2]))
            push!(values, parse(Float64, words[3]))
        end

        return sparse(rows, columns, values)
    end

    function ReadVector(file::IOStream) :: Vector{Float64}
        vector = []

        for line in Iterators.drop(eachline(file), 1)
            push!(vector, parse(Float64, line))
        end
            
        return vector
    end


    function calculateRightSide(M::SparseMatrixCSC{Float64,Int}, size::Int, blockSize::Int)
        ans = zeros(Float64, size)
    
        for i in 1:size
            startC = convert(Int, max(i - (2 + blockSize), 1))
            endC = convert(Int, min(i + blockSize, size))
    
            for j in startC:endC
                ans[i] += M[i, j]
            end
        end
            
        return ans
    end
    
    function Gauss(M:: SparseMatrixCSC{Float64,Int}, b :: Vector{Float64}, size :: Int, blockSize :: Int) :: Vector{Float64}
        result = zeros(Float64, size)

        for k in 1:size-1
            for i in k+1:min(size, k + blockSize + 1)
                z = M[i, k] / M[k, k]
                M[i, k] = 0.0

                for j in k+1:min(size, k + blockSize + 1)
                    M[i, j] -= z * M[k, j]
                end

                b[i] -= z * b[k]
            end
        end

        for i in size:-1:1
            currentSum = 0
            for j in i+1:min(size, i + blockSize + 2)
                currentSum += M[i, j] * result[j]
            end

            result[i] = (b[i] - currentSum) / M[i, i]
        end

        return result
    end

    function GaussWithPivots(M :: SparseMatrixCSC{Float64, Int}, b :: Vector{Float64}, size :: Int, blockSize :: Int) :: Vector{Float64}

        result = zeros(Float64, size)
        pivots = collect(1:size)

        for k in 1:size-1
            lastColumn = 0
            lastRow = 0

            for i in k:min(size, k + blockSize + 1)
                if abs(M[pivots[i], k]) > lastColumn
                    lastColumn = abs(M[pivots[i], k])
                    lastRow = i
                end
            end

            pivots[lastRow], pivots[k] = pivots[k], pivots[lastRow]

            for i in k+1:min(size, k + blockSize + 1)
                z = M[pivots[i], k] / M[pivots[k], k]
                M[pivots[i], k] = 0.0

                for j in k+1:min(size, k + 2 * blockSize)
                    M[pivots[i], j] = M[pivots[i], j] - z * M[pivots[k], j]
                end
                b[pivots[i]] = b[pivots[i]] - z * b[pivots[k]]
            end
        end

        for k in 1:size-1
            for i in k+1:min(size, k + 2 * blockSize)
                b[pivots[i]] = b[pivots[i]] - M[pivots[i], k] * b[pivots[k]]
            end
        end

        for i in size:-1:1
            currentSum = 0
            for j in i+1:min(size, i + 2 * blockSize)
                currentSum += M[pivots[i], j] * result[j]
            end
            result[i] = (b[pivots[i]] - currentSum) / M[pivots[i], i]
        end

        return result
    end

end