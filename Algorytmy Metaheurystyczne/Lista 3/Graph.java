import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;

public class Graph
{
    ArrayList<Vertex> vertices;
    ArrayList<Edge> edges;

    Graph()
    {
        vertices = new ArrayList<>();
        edges = new ArrayList<>();
    }

    List<Vertex> getNeighbors(int id)
    {
        List<Vertex> neighbors = new LinkedList<>();
        for(Edge edge : edges)
        {
            if(edge.src.id == id)
            {
                neighbors.add(edge.dest);
            }
            if(edge.dest.id == id)
            {
                neighbors.add(edge.src);
            }
        }
        return neighbors;
    }

    Vertex getVertex(int id)
    {
        return vertices.get(id);
    }
}
