#Szymon Pestrowicz 268496
module blocksys
    include("./matrixgen.jl")
    export ReadMatrix, ReadVector, Gauss, GaussWithPivots, runTest, calculateRightSide

    using  SparseArrays
    using .matrixgen
    using PyPlot

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