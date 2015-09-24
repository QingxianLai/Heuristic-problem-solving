import java.util.List;

/**
 * Created by LaiQX on 09/24/15.
 */
public class GreedySearch {
    private List<City> cities;
    boolean[] marked;

    public GreedySearch(List<City> cities) {
        this.cities = cities;
        marked = new boolean[cities.size()+1];
        Search();
    }

    private void Search() {
        City current = cities.get(0);

        double total = 0.0;

        while (true) {
            marked[current.getId()] = true;
            System.out.println(current.getId());
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
    }

    public static void main(String[] args) {
        GenerateCities f = new GenerateCities("src/travelingtest.txt");
        GreedySearch m = new GreedySearch(f.getCities());
    }


}
