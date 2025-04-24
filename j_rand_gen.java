import java.io.FileWriter;
import java.io.IOException;

public class Main {
    public static void main(String[] args) {
        try {
            FileWriter writer = new FileWriter("j_rand.txt");
            for(int i = 0; i < 128; i++)
            {
                int randInt = 0 + (int)(Math.random()*2);
                writer.write(String.valueOf(randInt));
            }
            writer.close();
        } catch (IOException e) {
            System.out.println("Ошибка при записи в файл");
            e.printStackTrace();
        }
    }
}