import java.io.FileNotFoundException;
import java.util.ArrayList;

public class L3Z1 {
    public static void main(String[] args) throws FileNotFoundException {
        final String[] files = {"xqf131.tsp", "xqg237.tsp", "pma343.tsp", "pka379.tsp", "bcl380.tsp", "pbl395.tsp", "pbk411.tsp", "pbn423.tsp", "pbm436.tsp", "xql662.tsp", "xit1083.tsp", "icw1483.tsp", "djc1785.tsp", "dcb2086.tsp", "pds2566.tsp"};

        for (String file : files) {
            System.out.println("Plik: " + file);

            Graph graph = GraphLoader.loadGraph("data/" + file);

            int populationSize = graph.vertices.size();
            int numOfGenerations = 10000;
            int minCost = Integer.MAX_VALUE;
            float avgCost = 0;
            // Parametry algorytmu genetycznego
            double crossoverProbability = 0.8;
            double mutationProbability = 0.01;

                for (int generation = 0; generation < numOfGenerations; generation++) {
                    // Krok 1: Generowanie populacji początkowej
                    ArrayList<Vertex[]> population = generateInitialPopulation(graph.vertices, populationSize);

                    for (int k = 0; k < populationSize; k++) {
                        // Krok 2: Ewaluacja i selekcja
                        Vertex[] parent1 = tournamentSelection(population);
                        Vertex[] parent2 = tournamentSelection(population);

                        // Krok 3: Krzyżowanie
                        Vertex[] child = crossover(parent1, parent2, crossoverProbability);

                        // Krok 4: Mutacja
                        if (Math.random() < mutationProbability) {
                            mutate(child);
                        }

                        int childCost = permutationCost(child);

                        if (childCost < minCost) {
                            minCost = childCost;
                        }

                        avgCost += childCost;
                    }
                }

            avgCost /= (numOfGenerations * populationSize * 100);

            System.out.println("Średnie rozwiązanie: " + avgCost);
            System.out.println("Najlepsze uzyskane rozwiązanie: " + minCost);

            System.out.println();
        }
    }

    private static ArrayList<Vertex[]> generateInitialPopulation(ArrayList<Vertex> vertices, int populationSize) {
        ArrayList<Vertex[]> population = new ArrayList<>();
        for (int i = 0; i < populationSize; i++) {
            Vertex[] solution = generateRandomSolution(vertices);
            population.add(solution);
        }
        return population;
    }

    private static Vertex[] generateRandomSolution(ArrayList<Vertex> vertices) {
        ArrayList<Vertex> copy = new ArrayList<>(vertices);
        Vertex[] solution = new Vertex[vertices.size()];
        int ptr = 0;
        while (!copy.isEmpty()) {
            int index = (int) (Math.random() * copy.size());
            solution[ptr] = copy.remove(index);
            ptr++;
        }
        return solution;
    }

    private static Vertex[] tournamentSelection(ArrayList<Vertex[]> population) {
        int tournamentSize = 3;
        Vertex[] best = null;
        for (int i = 0; i < tournamentSize; i++) {
            Vertex[] candidate = population.get((int) (Math.random() * population.size()));
            if (best == null || permutationCost(candidate) < permutationCost(best)) {
                best = candidate;
            }
        }
        return best;
    }

    private static Vertex[] crossover(Vertex[] parent1, Vertex[] parent2, double crossoverProbability) {
        if (Math.random() > crossoverProbability) {
            return parent1;
        }

        int size = parent1.length;
        Vertex[] child = new Vertex[size];

        int startPos = (int) (Math.random() * size);
        int endPos = (int) (Math.random() * (size - startPos)) + startPos;

        for (int i = startPos; i < endPos; i++) {
            child[i] = parent1[i];
        }

        int ptr = 0;
        for (int i = 0; i < size; i++) {
            if (child[i] == null) {
                while (containsVertex(child, parent2[ptr])) {
                    ptr++;
                }
                child[i] = parent2[ptr++];
            }
        }

        return child;
    }

    private static boolean containsVertex(Vertex[] array, Vertex vertex) {
        for (Vertex v : array) {
            if (v != null && v.equals(vertex)) {
                return true;
            }
        }
        return false;
    }

    private static void mutate(Vertex[] child) {
        int pos1 = (int) (Math.random() * child.length);
        int pos2 = (int) (Math.random() * child.length);

        swap(child, pos1, pos2);
    }

    private static void swap(Vertex[] array, int i, int j) {
        Vertex temp = array[i];
        array[i] = array[j];
        array[j] = temp;
    }

    private static int permutationCost(Vertex[] permutation) {
        int n = permutation.length;
        int cost = 0;
        for (int i = 0; i < n - 1; i++) {
            cost += (new Edge(permutation[i], permutation[i + 1])).weight;
        }
        cost += (new Edge(permutation[n - 1], permutation[0])).weight;

        return cost;
    }
}
