import java.util.List;

public class SimulatedAnnealing {
    private double temperature = 10000;
    private static final double COOLING_RATE = 0.005;
    private static final int CITY_NUMBER = 1000;
    private List<City> cities;

    public SimulatedAnnealing(List<City> cities) {
        this.cities = cities;
    }

    public double acceptProbability(double distanceDiff) {
        if (distanceDiff < 0) {
            return 1.0;
        } else {
            return 0; //Math.exp(-distanceDiff / temperature);
        }
    }
    
    public Tour simulatedAnnealing() {
        GreedySearch m = new GreedySearch(cities);
        Tour tour = new Tour(m.getPath());

        double initialDistance = tour.totalDistance();
        while (temperature > 1.0) {
            int pos1 = (int)(CITY_NUMBER * Math.random());
            int pos2 = (int)(CITY_NUMBER * Math.random());
            double diff = tour.distanceDiff(pos1, pos2);
            if (acceptProbability(diff) > Math.random()) {
                City temp = tour.getCity(pos1);
                tour.setCity(pos1, tour.getCity(pos2));
                tour.setCity(pos2, temp);
            }
            temperature -= temperature * COOLING_RATE; 
        }
        System.out.println(tour.totalDistance());
        return tour;
    }
    public static void main (String[] args) {
        GenerateCities f = new GenerateCities("src/travelingtest.txt");
        SimulatedAnnealing sa = new SimulatedAnnealing(f.getCities());
        sa.simulatedAnnealing();
    }
}
