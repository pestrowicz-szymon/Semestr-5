import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;

public class Encoding_LZ77 {

    Converter converter = new Converter();

    private final int k = 7; // rozmiar słownika
    private final int n = 6; // rozmiar bufora wejściowego

    StringBuilder dictionaryBuffer = new StringBuilder(k);
    StringBuilder encodingBuffer = new StringBuilder(n);
    StringBuilder bigBuffer = new StringBuilder();
    ArrayList<Tuple> encodedText = new ArrayList<>();


    public ArrayList<Tuple> encoding(String textToEncoding, String fileName) throws IOException {

        // initBuffers() tworzy początkowe bufory algorytmu
        // dictionaryBuffer - wypełnia go 1 znakiem z testu do zakodowania
        // encodingBuffer - wypełnia go znakami na miejscach od 1 do n
        // bigBuffer - dictionaryBuffer + encodingBuffer
        // przykładowy bigBuffer dla tekstu AXABRACADABRARRARRAX wygląda następująco:
        // AAAAAAAXABRACADABRARRARRAX
        initBuffers(textToEncoding);

        // pętla while działa tak długo jak jest jeszcze co wsadzić do encodingBuffera, czyli
        // dopóki nie zakodujemy całego tekstu
        while (encodingBuffer.length() != 0) {
            System.out.println("---------------------------");
            Tuple encodedTuple = oneStepOfEncoding();
            encodedText.add(encodedTuple);
        }

        getValuesDescribingTheCompression(textToEncoding, fileName);
        return encodedText;
    }


    public Tuple oneStepOfEncoding() {
        // pobieramy obecne bufory do zmiennych
        String dictionary = dictionaryBuffer.toString();
        String ourPattern = encodingBuffer.toString();


        System.out.println("Dictionary: " + dictionary);
        System.out.println("Our pattern: " + ourPattern);
        System.out.println("Running RabinKarpAlgorithm...");

        // w przypadku gdy pattern pokrywa się z dictionary to zapisujemy w nim parę (i, j)
        // gdzie i jest indexem początku elementu wspólnego, natomiast j jego długością
        // w przypadku gdy pattern nie ma części wspólnej z dictionary to będzie tam zapisane
        // (0, x) gdzie x jest pierwszym znakiem z ourPattern
        Tuple tupleToCheck = RabinKarpAlgorithm.searchAll(ourPattern, dictionary);
        System.out.println("tupleToCheck: ");
        Tuple.printTuple(tupleToCheck);

        if (tupleToCheck.getSecond() instanceof Character) {         //(0, letter_code)
            updateBuffers(1);
        } else {                                            //(i, j)
            int c = (int) tupleToCheck.getSecond();
            updateBuffers(c);
        }
        return tupleToCheck;
    }


    public void initBuffers(String textToEncoding) {
        dictionaryBuffer.append(String.valueOf(textToEncoding.charAt(0)).repeat(Math.max(0, dictionaryBuffer.capacity())));

//        dodatkowy warunek w pętli for, bo może zdażyć się sytuacja,
//        gdy długość tekstu do zakodawania jest mniejsza od długości bufora
        for (int i = 0; i < encodingBuffer.capacity() && i < textToEncoding.length() - 1; i++) {
            encodingBuffer.append(textToEncoding.charAt(i + 1));
        }

        bigBuffer.append(dictionaryBuffer);
        bigBuffer.append(encodingBuffer);
        if (n + 1 < textToEncoding.length()) {
            bigBuffer.append(textToEncoding.substring(n + 1));
        }


        encodedText.add(new Tuple(0, textToEncoding.charAt(0)));
    }

    public void updateBuffers(int j) {
        dictionaryBuffer = new StringBuilder(bigBuffer.substring(j, j + k));

        if (j + k + n < bigBuffer.length()) {
            encodingBuffer = new StringBuilder(bigBuffer.substring(j + k, j + k + n));
        } else {
            encodingBuffer = new StringBuilder(bigBuffer.substring(j + k));
        }
        bigBuffer = new StringBuilder(bigBuffer.substring(j));
    }


    public void getValuesDescribingTheCompression(String textToEncoding, String fileName) throws IOException {
        System.out.println("Wartości opisujące kompresję:");

        //długość kodowanego pliku
        int lengthOfTextToEncoding = textToEncoding.length();
        System.out.println("długość kodowanego pliku: " + lengthOfTextToEncoding);

        //długość uzyskanego kodu
        int lengthOfCode = encodedText.size();
        System.out.println("długość uzyskanego kodu: " + lengthOfCode);

        //stopień kompresji = dł przed skompresowaniem/dł po skompresowaniu
        System.out.println("stopień kompresji: " + (float) lengthOfTextToEncoding / lengthOfCode);

        //entropia kodowanego tekstu
        byte[] byteArray = converter.convertFileToByteArray(fileName);
        HashMap<Byte, Float> mapOfText = converter.getCzestosc(byteArray);
        double textEntropy = converter.calculatingEntropy1(mapOfText);
        System.out.println("entropia kodowanego tekstu: " + textEntropy);

        //entropia uzyskanego kodu
        HashMap<Tuple, Float> mapOfCode = converter.getCzestoscWarunkowa(encodedText);
        double codeEntropy = converter.calculatingEntropy2(mapOfCode);
        System.out.println("entropia uzyskanego kodu: " + codeEntropy);
    }


}

