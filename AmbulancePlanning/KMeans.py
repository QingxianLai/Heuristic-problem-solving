from random import randint

class Patient(object):
    def __init__(self, x, y, time):
        self.x = x
        self.y = y
        self.time = time
    
    def __repr__(self):
        return "x: " + str(self.x) + " y: " + str(self.y) + " time: " + str(self.time)

class KMeans(object):
    def __init__(self, file_name):
        self.file_name = file_name
        self.center_num = 5
        self.patients_num = -1
        self.centers = [[0, 0] for i in range(5)]
        self.data_set = []
        self.__parse_file()

    def __parse_file(self):
        try:
            with open(self.file_name, "r") as f:
                for line in f.readlines():
                    line = map(int, line.strip().split(","))
                    patient = Patient(line[0], line[1], line[2])
                    self.data_set.append(patient)
                f.close()
                self.patients_num = len(self.data_set)
        except Exception, e:
            raise e

    def __cal_distance(self, vector, patient):
        return abs(vector[0] - patient.x) + abs(vector[1] - patient.y)

    def __init_centers(self):
        for i in range(self.center_num):
            center = randint(0, self.patients_num - 1)
            self.centers[i] = [self.data_set[center].x, self.data_set[center].y]
    
    def k_means(self):
        cluster_assement = [[-1, -1] for i in range(self.patients_num)]
        cluster_changed = True

        self.__init_centers()
        while cluster_changed:
            cluster_changed = False
            for i in range(self.patients_num):
                min_dist = 100000
                min_index = 0
                for j in range(self.center_num):
                    cur_dist = self.__cal_distance(self.centers[j], self.data_set[i])
                    if cur_dist < min_dist:
                        min_dist = cur_dist
                        min_index = j

                if cluster_assement[i][0] != min_index:
                    cluster_changed = True
                    cluster_assement[i][0] = min_index
                    cluster_assement[i][1] = min_dist ** 2
            for j in range(self.center_num):
                patients_in_same_cluster = []
                for k in range(self.patients_num):
                    if cluster_assement[k][0] == j:
                        patients_in_same_cluster.append(self.data_set[j])
                x_total = 0.0
                y_total = 0.0
                for patient in patients_in_same_cluster:
                    x_total += patient.x
                    y_total += patient.y
                self.centers[j] = [x_total / len(patients_in_same_cluster), y_total / len(patients_in_same_cluster)]
        return self.centers, cluster_assement


def main():
    kmeans = KMeans("test.txt")
    centers, cluster_assement = kmeans.k_means() 
    print centers

if __name__ == '__main__':
    main()
