public class City {
    private int id;
    private int x;
    private int y;
    private int z;

    public City(int id, int x, int y, int z) {
        this.id = id;
        this.x = x;
        this.y = y;
        this.z = z;
    }

    public int getId() {
        return this.id;
    }

    public int getX() {
        return this.x;
    }

    public int getY() {
        return this.y;
    }

    public int getZ() {
        return this.z;
    }

    public double computeDistance(City city) {
        int xDistance = this.x - city.getX();
        int yDistance = this.y - city.getY();
        int zDistance = this.z - city.getZ();

        return Math.sqrt(xDistance * xDistance + yDistance * yDistance + zDistance * zDistance);
    }
}
