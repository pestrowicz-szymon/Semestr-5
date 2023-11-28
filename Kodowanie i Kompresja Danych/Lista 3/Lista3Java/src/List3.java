import java.io.*;
import java.util.ArrayList;

public class List3 {

    public static void main(String[] args) throws IOException {

        Encoding_LZ77 encoding_lz77 = new Encoding_LZ77();
        Decoding_LZ77 decoding_lz77 = new Decoding_LZ77();

//        String textToEncoding = "wabba-wabba-wabba-woo-woo-woo";

        String fileName = args[0];
        String textToEncoding = convertFileToString(fileName);

        if (textToEncoding.length() <= 1) {
            throw new IllegalArgumentException("Text to encoding must be longer than 1!");
        }

        ArrayList<Tuple> encodedText = encoding_lz77.encoding(textToEncoding, fileName);

//        for (Tuple tuple : encodedText) Tuple.printTuple(tuple);

        decoding_lz77.decoding(encodedText);

    }

    public static String convertFileToString(String fileName) throws IOException {
        InputStream is = new FileInputStream(fileName);
        BufferedReader buf = new BufferedReader(new InputStreamReader(is));
        String line = buf.readLine();
        StringBuilder sb = new StringBuilder();
        while (line != null) {
            sb.append(line).append("\n");
            line = buf.readLine();
        }
        return sb.toString();
    }


}
