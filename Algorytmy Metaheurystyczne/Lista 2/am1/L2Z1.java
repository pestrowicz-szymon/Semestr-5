import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Random;

public class L2Z1 {
    public static void main(String[] args) throws FileNotFoundException {
        final String[] files = {"xqf131.tsp", "xqg237.tsp", "pma343.tsp", "pka379.tsp", "bcl380.tsp", "pbl395.tsp", "pbk411.tsp", "pbn423.tsp", "pbm436.tsp"};//, "xql662.tsp", "xit1083.tsp", "icw1483.tsp", "djc1785.tsp", "dcb2086.tsp", "pds2566.tsp"};

        for (String file : files) {
            System.out.println("Plik: " + file);

            Graph graph = GraphLoader.loadGraph("data/" + file);

            Random random = new Random();

            int n = graph.vertices.size();
            int minCost = Integer.MAX_VALUE;
            float avgCost = 0;
            // Parametry algorytmu symulowanego wyżarzania
            double initialTemperature = 1000.0;
            double temperatureReductionFactor = 0.99;
            int attemptsPerEpoch = 50;

            Vertex[] bestSolution = null;

            for (int k = 0; k < n; k++) {
                ArrayList<Vertex> vertices = new ArrayList<>(graph.vertices);
                Vertex[] currentSolution = new Vertex[n];
                int ptr = 0;
                while (!vertices.isEmpty()) {
                    int index = random.nextInt(vertices.size());
                    currentSolution[ptr] = vertices.remove(index);
                    ptr++;
                }

                double temperature = initialTemperature;

                while (temperature > 1.0) {
                    for (int attempt = 0; attempt < attemptsPerEpoch; attempt++) {
                        Vertex[] neighbor = generateNeighbor(currentSolution);
                        int currentCost = permutationCost(currentSolution);
                        int neighborCost = permutationCost(neighbor);

                        if (neighborCost < currentCost || acceptWithProbability(temperature, currentCost, neighborCost)) {
                            currentSolution = neighbor;
                        }

                        if (neighborCost < minCost) {
                            minCost = neighborCost;
                            bestSolution = Arrays.copyOf(neighbor, neighbor.length);
                        }
                    }

                    temperature *= temperatureReductionFactor;
                }

                avgCost += permutationCost(bestSolution);
            }

            avgCost /= n;

            System.out.println("Średnie rozwiązanie: " + avgCost);
            System.out.println("Najlepsze uzyskane rozwiązanie: " + minCost);

            System.out.println();
        }
    }

    private static Vertex[] generateNeighbor(Vertex[] permutation) {
        Vertex[] neighbor = permutation.clone();
        Random random = new Random();
        int i = random.nextInt(permutation.length);
        int j = random.nextInt(permutation.length);
        swap(neighbor, i, j);
        return neighbor;
    }

    private static boolean acceptWithProbability(double temperature, int currentCost, int neighborCost) {
        if (neighborCost < currentCost) {
            return true;
        }
        double probability = Math.exp((currentCost - neighborCost) / temperature);
        return Math.random() < probability;
    }

    private static void swap(Vertex[] t, int i, int j) {
        Vertex tmp = t[i];
        t[i] = t[j];
        t[j] = tmp;
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
