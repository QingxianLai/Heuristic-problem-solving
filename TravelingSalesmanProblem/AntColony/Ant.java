import java.util.Set;
import java.util.HashSet;
import java.util.Random;
import java.util.List;
import java.util.ArrayList;

public class Ant {
    /* private Set<Integer> tabu; */
    private Set<Integer> allowedCities;
    private List<Integer> tour;
    private double[][] delta;
    private double[][] distance;
    private double alpha;
    private double beta;

    private double tourLength;
    private int cityNum;
    private int firstCity;
    private int currentCity;

    public Ant(int num) {  
        cityNum = num;  
        tourLength = 0;  
    }  

    public void init(double[][] distance, double alpha, double beta) {
        this.alpha = alpha;
        this.beta = beta;
        tour = new ArrayList<Integer>();
        /* tabu = new HashSet<Integer>(); */
        allowedCities = new HashSet<Integer>();
        this.distance = distance;
        delta = new double[cityNum][cityNum];
        for (int i = 0; i < cityNum; i++) {
            allowedCities.add(i);
        }
        Random random = new Random(System.currentTimeMillis());
        firstCity = random.nextInt(cityNum);
        allowedCities.remove(firstCity);
        /* tabu.add(firstCity); */
        currentCity = firstCity;
        tour.add(firstCity);
    }

    public void selectNextCity(double[][] pheromone) {
        double[] p = new double[cityNum];
        double sum = 0.0;
        for (Integer i: allowedCities) {
            sum += Math.pow(pheromone[currentCity][i], alpha) * Math.pow(1 / distance[currentCity][i], beta);
        }
        for (Integer i: allowedCities) {
            p[i] = Math.pow(pheromone[currentCity][i], alpha) * Math.pow(1 / distance[currentCity][i], beta) / sum;
        }
        Random random = new Random(System.currentTimeMillis());
        double selectP = random.nextDouble();
        int selectCity = 0;
        double sumP = 0;
        for (int i = 0; i < cityNum; i++) {
            sumP += p[i];
            if (sumP >= selectP) {
                selectCity = i;
                break;
            }
        }
        allowedCities.remove(selectCity);
        /* tabu.add(selectCity); */
        currentCity = selectCity;
        tour.add(selectCity);
    }

    private double calculateTourLength() {
        double sum = 0.0;
        for (int i = 0; i < cityNum - 1; i++) {
            sum += distance[tour.get(i)][tour.get(i + 1)];
        }
        return sum;
    }

    public Set<Integer> getAllowedCities() {
        return allowedCities;
    }

    /* public Set<Integer> getTabu() { */
    /*     return tabu; */
    /* } */
    
    public void swapTour(int i, int j) {
        Integer temp = tour.get(i);
        tour.set(i, tour.get(j));
        tour.set(j, temp);
    }

    public int getFirstCity() {  
        return firstCity;  
    }  

    public double getTourLength() {  
        tourLength = calculateTourLength();  
        return tourLength;  
    }  

    public List<Integer> getTour() {
        return tour;
    }

    public double[][] getDelta() {  
        return delta;  
    } 
    
    public void setDelta(double[][] delta) {  
        this.delta = delta;  
    }  
}
