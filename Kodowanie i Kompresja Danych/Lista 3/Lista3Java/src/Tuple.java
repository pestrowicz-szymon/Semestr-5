public class Tuple<First, Second> {

    private final First first;
    private final Second second;


    public Tuple(First first, Second second) {
        this.first = first;
        this.second = second;
    }

    public First getFirst() {
        return first;
    }

    public Second getSecond() {
        return second;
    }

    public static void printTuple(Tuple tuple) {
        System.out.println("(" + tuple.getFirst().toString() + ", " + tuple.getSecond().toString() + ")");
    }
}
