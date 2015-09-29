import java.util.*;

/**
 * Created by LaiQX on 09/25/15.
 */
public class primTree {
    private List<City> cities;

    public Graph primEulerGraph(List<City> cities){
        // return a minimum spanning tree, and it is also a eulerian graph.
        boolean[] marked = new boolean[cities.size()+1];
        Set<City> inTree = new HashSet<City>();

        this.cities = cities;
        Graph primT = new Graph(cities.size()+1);


        double treeLength = 0.0;


        City current = cities.get(1);
        while (true) {
            inTree.add(current);
            marked[current.getId()] = true;

            if (inTree.size() == cities.size()) {
                break;
            }

            City nearestFrom = null;
            City nearestTo = null;
            Double minDis = 1000000.0;
            for (City c: inTree) {
                for (City next: cities) {
                    if (marked[next.getId()]) {
                        continue;
                    }
                    if (minDis > c.computeDistance(next)) {
                        minDis = c.computeDistance(next);
                        nearestFrom = c;
                        nearestTo = next;
                    }
                }
            }

            if (nearestFrom == null) {
                break;
            }

            primT.addEdge(nearestFrom.getId(), nearestTo.getId(), nearestFrom.computeDistance(nearestTo));
            treeLength += nearestFrom.computeDistance(nearestTo);
            current = nearestTo;
        }

        System.out.println("tree Distance: " + treeLength);
        return primT;
    }


    public List<Integer> findEulerPath(Graph g){
        // make sure that g is a eulerian graph; Using Fleury's Algorithm

        int startCity = 100;
        int city = startCity;
        List<Integer> path = new ArrayList<Integer>();


        double EulerPathLength = 0.0;
        int line_Count = 1;

        while (true) {

            path.add(city);
            Set<Integer> nextCities = new HashSet<Integer>();
            int nextCity = 0;

            for (Edge e: g.adj(city)) {
                if (e.isDarken()) {
                    continue;
                }

                if (nextCities.contains(e.other(city))) {
                    nextCity = e.other(city);
                    e.dark();
                    break;
                } else {
                    nextCities.add(e.other(city));
                }
            }

            if (nextCity == 0) {
                if (nextCities.size()==0) {
                    break;
                } else {
                    for (Edge e: g.adj(city)) {
                        if (e.isDarken()) {
                            continue;
                        }
                        e.dark();
                        nextCity = e.other(city);
                        break;
                    }
                }
            }

            // debug
            double dis = cities.get(city-1).computeDistance(cities.get(nextCity-1));
            EulerPathLength += dis;
            System.out.println(line_Count + ". " + city+" => "+nextCity + " || distance: " + dis);
            line_Count ++;


            city = nextCity;

        }

        System.out.println("EulerPathLength = " + EulerPathLength);
        System.out.println("Euler path size = " + path.size());

        return path;
    }


    public double getTotalDistance(List<Integer> path) {
        boolean[] marked = new boolean[cities.size() + 1];
        double total = 0.0;

        int lastCity = 0;
        int currentCity = 1;
        marked[path.get(lastCity)] = true;

        int line_count = 1;

        while (currentCity < path.size()) {
            int current = path.get(currentCity);
            if (marked[current]) {
                currentCity++;
                continue;
            }

            int last = path.get(lastCity);
            double dis =  cities.get(last - 1).computeDistance(cities.get(current - 1));

            total += dis;

            // print
            System.out.println(line_count+ " : " + last + " => " + current+ " || distance: " + dis);
            line_count++;

            marked[current] = true;
            lastCity = currentCity;
            currentCity++;
        }
        return total;
    }


    public static void main(String[] args) {
        GenerateCities f = new GenerateCities("src/travelingtest.txt");
        primTree m = new primTree();
        List<City> cities = f.getCities();
        Graph g = m.primEulerGraph(cities);
        List<Integer> path = m.findEulerPath(g);
        double totalDistance = m.getTotalDistance(path);
        System.out.println(totalDistance);
    }
}

class Graph{
    private int V;
    private Collection<Edge>[] adj;

    public Graph(int V) {
        this.V = V;
        adj = (Collection<Edge>[]) new Collection[V];
        for (int v = 0; v< V; v++) {
            adj[v] = new ArrayList<Edge>();
        }
    }

    public int V() {
        return V;
    }

    public void addEdge(int v, int w, double weight) {
        Edge e1 = new Edge(v, w, weight);
        adj[v].add(e1);
        adj[w].add(e1);

        // to Make the graph a Eulerian graph
        Edge e2 = new Edge(v, w, weight);
        adj[v].add(e2);
        adj[w].add(e2);

    }

    public Iterable<Edge> adj(int v) {
        return adj[v];
    }
}


class Edge{
    private int v;
    private int w;
    private double weight;
    private boolean isDarken;

    Edge(int v, int w, double weight) {
        this.isDarken=false;
        this.v = v;
        this.w = w;
        this.weight = weight;
    }

    public double weight() {
        return weight;
    }

    public boolean isDarken(){
        return isDarken;
    }

    public void dark(){
        isDarken = true;
    }

    public int either() {
        return v;
    }

    public int other(int vertex) {
        if (vertex == v) return w;
        if (vertex == w) return v;
        return -1;
    }
}

