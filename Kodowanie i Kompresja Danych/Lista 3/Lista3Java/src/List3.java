import java.io.*;
import java.util.ArrayList;

public class List3 {

    public static void main(String[] args) throws IOException {

        Encoding_LZ77 encoding_lz77 = new Encoding_LZ77();
        Decoding_LZ77 decoding_lz77 = new Decoding_LZ77();

        String fileName = "src/test3.bin";
        String textToEncoding = convertFileToString(fileName);

        ArrayList<Tuple> encodedText = encoding_lz77.encoding(textToEncoding, fileName);

        //for (int i = 0; i < encodedText.size(); i++) {
        //    Tuple.printTuple(encodedText.get(i));
        //}

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
