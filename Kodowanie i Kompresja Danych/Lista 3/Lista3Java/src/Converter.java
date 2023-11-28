import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;


public class Converter {

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


    public ArrayList<Tuple> createListOfSymbolPairs(byte[] bytes) {

        ArrayList<Tuple> symbolPairs = new ArrayList<>();

        //dla pierwszego symbolu poprzedzające jest '0'
        Tuple tuple = new Tuple((byte) 0, bytes[0]);
        symbolPairs.add(tuple);


        for (int i = 1; i < bytes.length; i++) {
            tuple = new Tuple(bytes[i - 1], bytes[i]);
            symbolPairs.add(tuple);
        }

        return symbolPairs;
    }


    public HashMap<Tuple, Float> getCzestoscWarunkowa(ArrayList<Tuple> tuples) {
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

    public double calculatingConditionalEntropy(HashMap<Tuple, Float> mapConditional, HashMap<Byte, Float> mapNormal) {
        double H = 0;
        double h = 0;

        for (Map.Entry<Byte, Float> entryN : mapNormal.entrySet()) {

            for (Map.Entry<Tuple, Float> entryC : mapConditional.entrySet()) {
                double P = entryC.getValue();        //P(y|x)
                double I = log2(1 / P);
                h = h + P * I;
            }
            H = entryN.getValue() * h;
        }
        return H;
    }


    public static double log2(double N) {
        return (Math.log(N) / Math.log(2));
    }


    public static String readAllBytes(String filePath) {
        String content = "";

        try {
            content = new String(Files.readAllBytes(Paths.get(filePath)));
        } catch (IOException e) {
            e.printStackTrace();
        }
        return content;
    }


}
