import java.io.File;
import java.util.ArrayList;
import java.io.FileWriter;
import java.io.IOException;

public class Decoding_LZ77 {

    private final int k = 255;  // rozmiar slownika
    private final int n = 256;  // rozmiar bufora wejsciowego

    StringBuilder dictionaryBuffer = new StringBuilder(k);
    StringBuilder outputBuffer = new StringBuilder(n);


    public void decoding(ArrayList<Tuple> encodedText) {

        // bierzemy pierwszego tupla i wywolujemy funkcje initBuffers, czyli
        // wstawiamy ja k razy do dictionary oraz 1 raz do outputBuffera
        initBuffers(encodedText.get(0));

        // nastepnie od 1 tupla az do konca wywolujemy oneStepOfDecoding
        for (int i = 1; i < encodedText.size(); i++) {
            oneStepOfDecoding(encodedText.get(i));
        }

        // zapisz zdekodowany tekst do pliku
        writeDecodedTextToFile(outputBuffer);
//        System.out.println(outputBuffer.toString());
    }


    public void initBuffers(Tuple tuple) {
        String firstLetter = tuple.getSecond().toString();
        dictionaryBuffer.append(String.valueOf(firstLetter).repeat(Math.max(0, dictionaryBuffer.capacity())));
        outputBuffer.append(firstLetter);
    }

    public void oneStepOfDecoding(Tuple tuple) {

        String newLetters;

        // jezeli na 2 miejscu jest litera to znaczy ze nie wykorzystamy wlasnosci kodowania
        // i ze bedziemy wpisywac nastepny znak w "tradycyjny" sposob
        if (tuple.getSecond() instanceof Character) {   //(0, kod_litery)
            newLetters = tuple.getSecond().toString();

            //przesun o 1 i dodaj nowe litery
            dictionaryBuffer = new StringBuilder(dictionaryBuffer.substring(1) + newLetters);
        } else {                                        //(i, j)
            int p = (int) tuple.getFirst();     // pozycja od ktorej kopiujemy
            int c = (int) tuple.getSecond();    // ile kopiujemy
            newLetters = dictionaryBuffer.substring(p, p + c);  // kopiujemy od p do p+c ze slownika

            //przesun o c i dodaj nowe litery
            dictionaryBuffer = new StringBuilder(dictionaryBuffer.substring(c) + newLetters);
        }
        // dodaj nowo znalezione litery do outputu
        outputBuffer.append(newLetters);
    }

    public void writeDecodedTextToFile(StringBuilder output) {

        try {
            File myObj = new File("decodedText.txt");
            myObj.createNewFile();
        } catch (IOException e) {
            System.out.println("An error occurred.");
            e.printStackTrace();
        }

        try {
            FileWriter myWriter = new FileWriter("decodedText.txt");
            myWriter.write(output.toString());
            myWriter.close();
        } catch (IOException e) {
            System.out.println("An error occurred");
            e.printStackTrace();
        }
    }
}
