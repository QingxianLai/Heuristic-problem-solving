import java.io.BufferedReader;
import java.io.IOException;
import java.io.FileInputStream;
import java.io.InputStreamReader;
import java.util.List;
import java.util.ArrayList;

public class GenerateCities {
    private String fileName;
    public List<City> tour;
    public GenerateCities(String fileName) {
        this.fileName = fileName;
        tour = new ArrayList<City>();
    }

    public List<City> getCities() {
        try {
            FileInputStream fstream = new FileInputStream(this.fileName);
            BufferedReader br = new BufferedReader(new InputStreamReader(fstream));
            for(String line; (line = br.readLine()) != null; ) {
                String[] cur = line.split(" ");
                City city = new City(Integer.parseInt(cur[0]), Integer.parseInt(cur[1]), Integer.parseInt(cur[2]), Integer.parseInt(cur[3]));
//                System.out.println("id: " + cur[0] + " x: " + cur[1] + " y: " + cur[2] + " z: " + cur[3]);
                tour.add(city);
            }
        } catch (IOException e) {
            e.printStackTrace();                    
        }
        return tour;
    }


}
