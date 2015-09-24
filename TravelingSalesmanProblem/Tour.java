import java.util.ArrayList;
import java.util.Collections;

public class Tour {
    private static final int CITY_NUMBER = 1000;
    public List<City> tour;
    
    public Tour(List<City> tour) {
        this.tour = new ArrayList<City>(tour);
    }

    public City getCity(int position) {
        return tour.get(position);
    }

    public void setCity(int position, City city) {
        tour.set(position, city);
    }

    public void shuffleTour() {
        Collections.shuffle(tour);
    }

    public double totalDistance() {
        double distance = 0;
        for (int i = 0; i < tour.size() - 1; i++) {
            distance += tour.get(i).computeDistance(tour.get(i + 1));
        }
        return distance;
    }

    public double distanceChange(int pos1, int pos2) {
        if (pos1 == pos2) {
            return 0.0;
        }
        if (pos1 > pos2) {
            return distanceChange(pos2, pos1);
        }
        if (pos1 == 0) {
            if (pos2 == CITY_NUMBER - 1) {
                return (tour.get(CITY_NUMBER - 1).computeDistance(tour.get(1)) + tour.get(0).computeDistance(tour.get(CITY_NUMBER - 2))) - (tour.get(0).computeDistance(tour.get(1)) + tour.get(CITY_NUMBER - 2).computeDistance(tour.get(CITY_NUMBER - 1)));
            } else {
                return (tour.get(0).computeDistance(tour.get(pos2 - 1)) + tour.get(0).computeDistance(tour.get(pos + 1)) + tour.get(pos2).computeDistance(tour.get(1))) - (tour.get(0).computeDistance(tour.get(1)) + tour.get(pos2 - 1).computeDistance(tour.get(pos2)) + tour.get(pos2).computeDistance(tour.get(pos2 + 1)));
            }
        } else {
            if (pos2 == CITY_NUMBER - 1) {
                return (tour.get(CITY_NUMBER - 2).computeDistance(tour.get(pos1)) + tour.get(pos1 - 1).computeDistance(tour.get(CITY_NUMBER - 1)) + tour.get(CITY_NUMBER - 1).computeDistance(tour.get(pos1 + 1))) - (tour.get(CITY_NUMBER - 2).computeDistance(tour.get(CITY_NUMBER - 1)) + tour.get(pos1 - 1).computeDistance(tour.get(pos1)) + tour.get(pos1).computeDistance(tour.get(pos1 + 1)));
            } else {
                return (tour.get(pos2 - 1).computeDistance(tour.get(pos1)) + tour.get(pos1).computeDistance(tour.get(pos2 + 1)) + tour.get(pos1 - 1).computeDistance(tour.get(pos2)) + tour.get(pos2).computeDistance(tour.get(pos1 + 1))) - (tour.get(pos2 - 1).computeDistance(tour.get(pos2)) + tour.get(pos2).computeDistance(tour.get(pos2 + 1)) + tour.get(pos1 - 1).computeDistance(tour.get(pos1)) + tour.get(pos1).computeDistance(tour.get(pos1 + 1)));
            }
        }
    }
}
