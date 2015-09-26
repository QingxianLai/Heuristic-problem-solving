import java.util.ArrayList;
import java.util.List;

/**
 * Created by LaiQX on 09/24/15.
 */
public class GreedySearch {
    private List<City> cities;
    boolean[] marked;
    private List<City> Path;

    public GreedySearch(List<City> cities) {
        this.cities = cities;
        marked = new boolean[cities.size()+1];
//        double min = 10000000.0;
//        int minStart = 0;
//        for(int i = 0; i< 100; i++) {
//            double res = Search(i);
//            System.out.println(res);
//
//            if (min >res) {
//                min = res;
//                minStart = i;
//            }
//        }
//
//        System.out.println("min: " + min);
//        System.out.println("minStart: " + minStart);
        Search(0);
    }

    public List<City> getPath(){
        return Path;
    }

    private double Search(int start) {
        Path = new ArrayList<City>();
        marked = new boolean[cities.size()+1];
        City current = cities.get(start);

        double total = 0.0;

        while (true) {
            marked[current.getId()] = true;
//            System.out.println(current.getId());
            Path.add(current);
            double min = 100000.0;
            City nearestCity = null;
            for (City c: cities) {
                if (marked[c.getId()]) {
                    continue;
                }
                double dis = current.computeDistance(c);
                if (dis<min) {
                    min =dis;
                    nearestCity = c;
                }
            }
            if (nearestCity == null) {
                break;
            }
            total += min;
            current = nearestCity;
        }

        System.out.println("total distance: "+ total);
        return total;
    }

    public static void main(String[] args) {
        GenerateCities f = new GenerateCities("src/travelingtest.txt");
        GreedySearch m = new GreedySearch(f.getCities());
    }


}
