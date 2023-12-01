import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;


public class Converter {

    // zwraca ciąg bitów reprezentujący plik fileName
    public byte[] convertFileToByteArray(String fileName) throws IOException {
        File file = new File(fileName);
        return Files.readAllBytes(file.toPath());
    }

    public HashMap<Byte, Float> getCzestosc(byte[] byteArray) {
        HashMap<Byte, Float> map = new HashMap<>();
        int length = byteArray.length;

        for (Byte keyToBeChecked : byteArray) {
            boolean isKeyInMap = map.containsKey(keyToBeChecked);

            //klucza nie ma w mapie i trzeba go dodać
            if (!isKeyInMap) {
                map.put(keyToBeChecked, (float) (1.0 / length));

            } else {             //klucz jest w mapie i zwiększamy il wystąpień
                Float actualValue = map.get(keyToBeChecked);
                Float newValue = actualValue + (float) (1.0 / length);
                map.replace(keyToBeChecked, newValue);
            }
        }
        return map;
    }

    public HashMap<Tuple, Float> getCzestoscTupli(ArrayList<Tuple> tuples) {
        HashMap<Tuple, Float> map = new HashMap<>();
        int length = tuples.size();

        for (Tuple actTuple : tuples) {
            Tuple whatTupleIsInMap = isTupleInMap(map, actTuple);

            if (whatTupleIsInMap == null) {
                map.put(actTuple, (float) (1.0 / length));
            } else {
                Float actualValue = map.get(whatTupleIsInMap);
                Float newValue = actualValue
                        + (float) (1.0 / length);
                map.replace(actTuple, newValue);
            }
        }
        return map;
    }


    public Tuple isTupleInMap(HashMap<Tuple, Float> map, Tuple tupleToCheck) {

        for (Tuple tuple : map.keySet()) {
            if (tupleToCheck.getFirst() == tuple.getFirst() && tupleToCheck.getSecond() == tuple.getSecond()) {
                return tuple;
            }
        }
        return null;
    }

    //te 2 metody powinny być jedną z jakimś generykiem...
    public double calculatingEntropy1(HashMap<Byte, Float> map) {
        double H = 0.0;

        for (Map.Entry<Byte, Float> entry : map.entrySet()) {
            float P = entry.getValue();
            H = H + P * log2(P);
        }
        H *= -1;
        return H;
    }


    public double calculatingEntropy2(HashMap<Tuple, Float> map) {
        double H = 0.0;

        for (Map.Entry<Tuple, Float> entry : map.entrySet()) {
            float P = entry.getValue();
            H = H + P * log2(P);
        }
        H *= -1;
        return H;
    }

    public static double log2(double N) {
        return (Math.log(N) / Math.log(2));
    }
}
