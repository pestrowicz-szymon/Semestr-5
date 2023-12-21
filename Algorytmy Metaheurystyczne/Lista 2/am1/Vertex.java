public class Vertex
{
    int id, x, y;

    Vertex(int id, int x, int y)
    {
        this.id = id;
        this.x = x;
        this.y = y;
    }

    @Override
    public String toString()
    {
        return id + 1 + ". (" + x + ", " + y + ")";
    }
}
