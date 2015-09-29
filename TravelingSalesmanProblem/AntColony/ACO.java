import java.util.List;
import java.util.LinkedList;
import java.io.IOException;

public class ACO {
    private Ant[] ants;
    private int antNum;  
    private int cityNum; 
    private int MAX_GEN; 
    private double[][] pheromone;
    private double[][] distance;   
    private double bestLength; 
    private int[] bestTour;  
    private List<City> cities;  
    
    private double alpha;  
    private double beta;  
    private double rho;  

    public ACO(int n, int m, int g, double a, double b, double r) {  
        cityNum = n;  
        antNum = m;  
        ants = new Ant[antNum];  
        MAX_GEN = g;  
        alpha = a;  
        beta = b;  
        rho = r;  
    }  

    private void init(String filename) throws IOException {
        GenerateCities f = new GenerateCities(filename);
        this.cities = f.getCities();
        distance = new double[cityNum][cityNum];
        for (int i = 0; i < cityNum; i++) {
            distance[i][i] = 0.0;
            for (int j = i + 1; j < cityNum; j++) {
                double dis = cities.get(i).computeDistance(cities.get(j));
                distance[i][j] = dis;
                distance[j][i] = dis;
            }
        }
        pheromone = new double[cityNum][cityNum];
        for (int i = 0; i < cityNum; i++) {
            for (int j = 0; j < cityNum; j++) {
                pheromone[i][j] = 0.1;
            }
        }
        bestLength = Integer.MAX_VALUE;
        bestTour = new int[cityNum];
        
        for (int i = 0; i < antNum; i++) {  
            ants[i] = new Ant(cityNum);  
            ants[i].init(distance, alpha, beta);  
        }  
    }

    public List<City> solve() {
        for (int g = 0; g < 3; g++) {
            for (int i = 0; i < antNum; i++) {
                for (int j = 1; j < cityNum; j++) {
                    ants[i].selectNextCity(pheromone);
                }
                /* ants[i].getTour().add(ants[i].getFirstCity()); */
                double curDistance = ants[i].getTourLength();
                
                if (curDistance < bestLength) {  
                    boolean finish = false;
                    while (!finish) {
                        boolean start = false;
                        for (int m = 0; m < cityNum - 1; m++) {
                            for (int n = m + 1; n < cityNum; n++) {
                                ants[i].swapTour(n, m);
                                double newDistance = ants[i].getTourLength();
                                if (newDistance < curDistance) {
                                    curDistance = newDistance;
                                    start = true;
                                    break;
                                } else {
                                    ants[i].swapTour(n, m);
                                }
                            }
                            if (start) {
                                break;
                            }
                        }
                        finish = true;
                    }
                    bestLength = curDistance;  
                    /* System.out.println(bestLength); */
                    for (int k = 0; k < cityNum; k++) {           
                        bestTour[k] = ants[i].getTour().get(k);  
                        /* System.out.print(ants[i].getTour().get(k) + " "); */
                    }  
                    /* System.out.println(); */
                } 
                
                for (int j = 0; j < cityNum - 1; j++) { 
                    ants[i].getDelta()[ants[i].getTour().get(j)][ants[i].getTour().get(j + 1)] = (1. / ants[i].getTourLength());  
                    ants[i].getDelta()[ants[i].getTour().get(j + 1)][ants[i].getTour().get(j)] = (1. / ants[i].getTourLength());  
                }  
            }
            updatePheromone();
            for (int i = 0; i < antNum; i++) {  
                ants[i].init(distance, alpha, beta);  
            }  
        }
        /* System.out.println("The optimal length is: " + bestLength); */
        List<City> newPath = new LinkedList<City>();
        for (int i = 0; i < cityNum; i++) {
            newPath.add(cities.get(bestTour[i]));
        }
        return newPath;
    }

    private void updatePheromone() {  
        for (int i = 0; i < cityNum; i++)  
            for (int j = 0; j < cityNum; j++)  
                pheromone[i][j] = pheromone[i][j] * (1 - rho);  
        for (int i = 0; i < cityNum; i++) {  
            for (int j = 0; j < cityNum; j++) {  
                for (int k = 0; k < antNum; k++) {  
                    pheromone[i][j] += ants[k].getDelta()[i][j];  
                }  
            }  
        }  
    }  
    public static void main(String[] args) throws IOException {  
        System.out.println("Start....");  
        ACO aco = new ACO(1000, 70, 150, 1.0, 70, 0.6);  
        aco.init("travelingtest.txt");  
        aco.solve();  
    }  
}
