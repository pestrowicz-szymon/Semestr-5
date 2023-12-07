import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;

public class Encoding_LZ77 {

    Converter converter = new Converter();

    private final int k = 255; // rozmiar słownika
    private final int n = 256; // rozmiar bufora wejściowego

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
            Tuple encodedTuple = singleStepOfEncoding();
            encodedText.add(encodedTuple);
        }

        printValues(textToEncoding, fileName);
        return encodedText;
    }


    public Tuple singleStepOfEncoding() {
        // pobieramy obecne bufory do zmiennych
        String dictionary = dictionaryBuffer.toString();
        String ourPattern = encodingBuffer.toString();

        // w przypadku gdy pattern pokrywa się z dictionary to zapisujemy w nim parę (i, j)
        // gdzie i jest indexem początku elementu wspólnego, natomiast j jego długością
        // w przypadku gdy pattern nie ma części wspólnej z dictionary to będzie tam zapisane
        // (0, x) gdzie x jest pierwszym znakiem z ourPattern
        Tuple tupleToCheck = RabinKarpAlgorithm.searchAll(ourPattern, dictionary);

        // jezeli w tuple na drugim miejscu jest litera to znaczy ze nie znalezlismy czesci
        // wspolnej patternu ze slownikiem, jezeli z kolei byla cyfra to znaczy ze znalezlismy
        // czesc wspolna i na tej podstawie odswiezamy wszystkie 3 bufory na 2 rozne sposoby
        if (tupleToCheck.getSecond() instanceof Character) {         //(0, letter_code)
            updateBuffers(1);
        } else {                                            //(i, j)
            int c = (int) tupleToCheck.getSecond();
            updateBuffers(c);
        }
        // zwraca znalezionego tupla
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
        // dictionaryBuffer pobieramy z bigBuffera, poniewaz on zawsze na poczatku zawiera nasz dictionary
        // zaczynamy od miejsca j'tego gdzie j to ilosc znakow ktore zakodowalismy w poprzednim ruchu a zbieramy
        // nowy dictionaryBuffer do j+k poniewaz k to jego rozmiar
        dictionaryBuffer = new StringBuilder(bigBuffer.substring(j, j + k));

        // encodingBuffer odswiezamy po sprawdzeniu czy odczytanie n (jego rozmiar) znakow z bigBuffera jest
        // jeszcze mozliwe, jesli tak to odczytujemy od miejsca j+k (koniec dictionary) to j+k+n (koniec dictionary
        // + rozmiar encodingBuffera). Natomiast jezeli nie mamy juz n znakow w zapasie to odczytujemy od konca
        // dictionary az do konca
        if (j + k + n < bigBuffer.length()) {
            encodingBuffer = new StringBuilder(bigBuffer.substring(j + k, j + k + n));
        } else {
            encodingBuffer = new StringBuilder(bigBuffer.substring(j + k));
        }
        // usuwamy j pierwszych znakow z bigBuffera
        bigBuffer = new StringBuilder(bigBuffer.substring(j));
    }


    public void printValues(String textToEncoding, String fileName) throws IOException {
        //długość kodowanego pliku
        int lengthOfTextToEncoding = textToEncoding.length();
        System.out.println("długość kodowanego pliku: " + lengthOfTextToEncoding);

        //długość uzyskanego kodu
        int lengthOfCode = encodedText.size();
        System.out.println("długość uzyskanego kodu: " + lengthOfCode);

        //stopień kompresji = długość przed skompresowaniem/długość po skompresowaniu
        System.out.println("stopień kompresji: " + (float) lengthOfTextToEncoding / lengthOfCode);

        //entropia kodowanego tekstu
        byte[] byteArray = converter.convertFileToByteArray(fileName);
        HashMap<Byte, Float> mapOfText = converter.getCzestosc(byteArray);
        double textEntropy = converter.calculatingEntropy1(mapOfText);
        System.out.println("entropia kodowanego tekstu: " + textEntropy);

        //entropia uzyskanego kodu
        HashMap<Tuple, Float> mapOfCode = converter.getCzestoscTupli(encodedText);
        double codeEntropy = converter.calculatingEntropy2(mapOfCode);
        System.out.println("entropia uzyskanego kodu: " + codeEntropy);
    }


}

