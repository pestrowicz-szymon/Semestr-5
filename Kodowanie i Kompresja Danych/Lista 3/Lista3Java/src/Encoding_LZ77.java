import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;

public class Encoding_LZ77 {

    Converter converter = new Converter();

    private final int k = 255;
    private final int n = 256;

    StringBuilder dictionaryBuffer = new StringBuilder(k);
    StringBuilder encodingBuffer = new StringBuilder(n);
    StringBuilder bigBuffer = new StringBuilder();
    ArrayList<Tuple> encodedText = new ArrayList<>();


    public ArrayList<Tuple> encoding(String textToEncoding, String fileName) throws IOException {

        initBuffers(textToEncoding);

        while (encodingBuffer.length() != 0) {
            Tuple encodedTuple = oneStepOfEncoding();
            encodedText.add(encodedTuple);
        }

        getValuesDescribingTheCompression(textToEncoding, fileName);
        return encodedText;
    }


    public Tuple oneStepOfEncoding() {
        String dictionary = dictionaryBuffer.toString();
        String ourPattern = encodingBuffer.toString();

        Tuple tupleToCheck = RabinKarpAlgorithm.searchAll(ourPattern, dictionary);

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

