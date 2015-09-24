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
            return Math.exp(distanceDiff / temperature);
        }
    }
    
    public Tour simulatedAnnealing() {
        Tour tour = new Tour(cities);
        tour.shuffleTour();
        double initialDistance = tour.totalDistance();
        while (temperature > 1.0) {
            int pos1 = (int)(CITY_NUMBER * Math.random());
            int pos2 = (int)(CITY_NUMBER * Math.random());
            double diff = tour.distanceDiff(pos1, pos2);
            if (acceptProbability(diff) > Math.random()) {
                City temp = tour.get(pos1);
                tour.setCity(pos1, tour.get(pos2));
                tour.setCity(pos2, temp);
            }
            temperature -= temperature * COOLING_RATE; 
        }
        return tour;
    }
}
