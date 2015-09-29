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
        double min = 10000000.0;
        int minStart = 0;
        for(int i = 0; i< cities.size(); i++) {
            double res = Search(i);
            //System.out.println(res);

            if (min > res) {
                min = res;
                minStart = i;
            }
        }
        Search(minStart);
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
            double min = 1000000.0;
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
        return total;
//        System.out.println("total distance: "+ total);
    }
}
