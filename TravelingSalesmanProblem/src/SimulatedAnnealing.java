import java.util.List;
import java.io.*;
public class SimulatedAnnealing {
    private double temperature;
    private static double COOLING_RATE = 0.001;
    private static int CITY_NUMBER = 1000;
    private List<City> cities;
    private Tour tour;
    public Tour bestTour;
    private int i = 1;
    public SimulatedAnnealing(List<City> cities) {
        this.cities = cities;
        GreedySearch m = new GreedySearch(cities);
        tour = new Tour(m.getPath());
        CITY_NUMBER = tour.tour.size();
        bestTour = new Tour(m.getPath());
    }

    public double acceptProbability(double distanceDiff) {
        if (distanceDiff < 0) {
            return 1.0;
        } else {
            return  Math.exp(-distanceDiff / temperature);
        }
    }
    
    public void simulatedAnnealing() {
        temperature = 35; 
        double min = 2000000.0;
        System.out.println("initial distance: " + tour.totalDistance());
        while (temperature > 8.0) {
            for (int i = 0; i < 500; i++) {
                
                int pos1 = (int)(CITY_NUMBER * Math.random());
                int pos2 = (int)(CITY_NUMBER * Math.random());
                double diff = tour.distanceDiff(pos1, pos2);
                City citySwap1 = tour.getCity(pos1);
                City citySwap2 = tour.getCity(pos2);

                tour.setCity(pos1, citySwap2);
                tour.setCity(pos2, citySwap1);
                if (acceptProbability(diff) < Math.random()) {
                    tour.setCity(pos1, citySwap1);
                    tour.setCity(pos2, citySwap2);
                }
                double curDistance = tour.totalDistance();
                if (curDistance < min) {
                    min = Math.min(min, curDistance);    
                    bestTour = new Tour(tour.tour);
                }
                
             
            }
            temperature -= temperature * COOLING_RATE;
        }
    }

    public void TwoOpt() {
        for (int m = 0; m < CITY_NUMBER - 1; m++) {
            for (int n = m + 1; n < CITY_NUMBER; n++) {
                double diff = bestTour.distanceDiff(m, n);
                City citySwap1 = bestTour.getCity(m);
                City citySwap2 = bestTour.getCity(n);
                bestTour.setCity(n, citySwap1);
                bestTour.setCity(m, citySwap2);
                if (diff > 0) {
                    bestTour.setCity(n, citySwap2);
                    bestTour.setCity(m, citySwap1);
                }
            }
        }
    }

    public static void main (String[] args) {
        GenerateCities f = new GenerateCities(args[0]);
        SimulatedAnnealing sa = new SimulatedAnnealing(f.getCities());
        for (int i = 0; i < 2; i++) {
            sa.simulatedAnnealing();     
        }    
        sa.TwoOpt();
        for (City city: sa.bestTour.tour) {
            System.out.println(city.getId());
        }
    }
}
