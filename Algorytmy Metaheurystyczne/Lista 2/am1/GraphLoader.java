import java.io.File;
import java.io.FileNotFoundException;
import java.util.Comparator;
import java.util.Scanner;

public class GraphLoader
{
    static Graph loadGraph(String file) throws FileNotFoundException
    {
        Graph graph = new Graph();
        Scanner reader = new Scanner(new File(file));
        while (reader.hasNextLine())
        {
            String line = reader.nextLine();
            if(!Character.isDigit(line.charAt(0)))
                continue;

            String[] split = line.split(" ");
            graph.vertices.add(new Vertex(graph.vertices.size(), Integer.parseInt(split[1]), Integer.parseInt(split[2])));
        }
        int v = graph.vertices.size();
        for(int i = 0; i < v - 1; i++)
        {
            for(int j = i + 1; j < v; j++)
            {
                graph.edges.add(new Edge(graph.vertices.get(i), graph.vertices.get(j)));
            }
        }

        graph.edges.sort(Comparator.comparingInt(o -> o.weight));

        return graph;
    }
}
