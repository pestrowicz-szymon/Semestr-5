using LinearAlgebra

function hilb(n::Int)
    # Function generates the Hilbert matrix  A of size n,
    #  A (i, j) = 1 / (i + j - 1)
    # Inputs:
    #	n: size of matrix A, n>=1
    #
    #
    # Usage: hilb(10)
    #
    # Pawel Zielinski
    if n < 1
        error("size n should be >= 1")
    end
    return [1 / (i + j - 1) for i in 1:n, j in 1:n]
end

function matcond(n::Int, c::Float64)
# Function generates a random square matrix A of size n with
# a given condition number c.
# Inputs:
#	n: size of matrix A, n>1
#	c: condition of matrix A, c>= 1.0
#
# Usage: matcond(10, 100.0)
#
# Pawel Zielinski
    if n < 2
        error("size n should be > 1")
    end
    if c< 1.0
        error("condition number  c of a matrix  should be >= 1.0")
    end
    (U,S,V)=svd(rand(n,n))
    return U*diagm(0 =>[LinRange(1.0,c,n);])*V'
end

# A - macierz n x n; b - wektor n-elementowy
function hilbert()
    println("\n HILBERT MATRIX \n");
    for n=1:20
        A = hilb(n);
        x = ones(n);

        b = A * x;

        resultdiv = A\b;
        resultpow = inv(A) * b;
        println("n = ",n, " ");
        println("rzad macierzy(A): ",rank(A));
        println("wskaznik uwarunkowania: ",cond(A))
        println("Result A/b: ", norm(x - resultdiv)/norm(x));
        println("Result A^-1*b: ", norm(x - resultpow)/norm(x));
        println();
    end
end

function randomM()

    println("\n RANDOM MATRIX \n");
    condM = [0.0, 1.0, 3.0, 7.0, 12.0, 16.0];
    number = [5, 10, 20];
  
    for i=1:3
        for j=1:6
            A = matcond(number[i], 10.0 ^ condM[j]);
            x = ones(number[i]);
            
            b = A * x;
            
            resultdiv = A\b;
            resultpow = inv(A) * b;
            println("rzad macierzy: ",rank(A));
            println("wskaznik uwarunkowania: ",cond(A))
            println("n: ",number[i])
            println("Result A/b: ", norm(x - resultdiv)/norm(x));
            println("Result A^-1 *b: ", norm(x - resultpow)/norm(x));
            println();
        end
    end
end

hilbert()
randomM()