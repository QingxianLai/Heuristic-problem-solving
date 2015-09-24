import java.io.BufferedReader;
import java.io.IOException;
import java.io.FileInputStream;
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
        FileInputStream fstream = new FileInputStream(this.fileName);
        try(BufferedReader br = new BufferedReader(new InputStreamReader(fstream)) {
            for(String line; (line = br.readLine()) != null; ) {
                String[] cur = line.split(" ");
                City city = new City(cur[0], cur[1], cur[2], cur[3]);
                tour.add(city);
            }
        } catch (IOException e) {
            e.printStackTrace();                    
        }
        return tour
    }
}
