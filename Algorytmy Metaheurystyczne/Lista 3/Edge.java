public class Edge
{
    Vertex src, dest;
    int weight;

    Edge(Vertex src, Vertex dest)
    {
        this.src = src;
        this.dest = dest;

        this.weight = (int) Math.round(Math.sqrt((src.x - dest.x) * (src.x - dest.x) + (src.y - dest.y) * (src.y - dest.y)));
    }

    @Override
    public String toString()
    {
        return src +  " -> " + dest + " : " + weight;
    }
}
