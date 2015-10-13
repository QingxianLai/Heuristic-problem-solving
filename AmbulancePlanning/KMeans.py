import random
from input import *
import collections
import operator
import itertools

class KMeans(object):
    def __init__(self, file_name):
        self.file_name = file_name
        self.center_num = 5
        self.patients_num = 300
        self.centers = [[0, 0] for i in range(5)]
        self.patients = []
        self.hospitals = []
        self.hospitals_patients = {}

    def __init_patients_hospitals(self):
        self.patients, self.hospitals = read_from_file(self.file_name)
        self.hospitals = sorted(self.hospitals, key=operator.attrgetter('ambu'))

    def __cal_distance(self, vector, patient):
        return abs(vector[0] - patient.x) + abs(vector[1] - patient.y)

    def __init_centers(self):
        random_sample = random.sample(range(0, self.patients_num - 1), 5)
        for i in range(len(random_sample)):
            self.centers[i] = [self.patients[random_sample[i]].x, self.patients[random_sample[i]].y]
    
    def k_means(self):
        self.__init_patients_hospitals()
        cluster_assement = [[-1, -1] for i in range(self.patients_num)]
        cluster_changed = True

        self.__init_centers()
        while cluster_changed:
            cluster_changed = False
            for i in range(self.patients_num):
                min_dist = 100000
                min_index = 0
                for j in range(self.center_num):
                    cur_dist = self.__cal_distance(self.centers[j], self.patients[i])
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
                        patients_in_same_cluster.append(self.patients[j])
                x_total = 0
                y_total = 0
                for patient in patients_in_same_cluster:
                    x_total += patient.x
                    y_total += patient.y
                self.centers[j] = [x_total / len(patients_in_same_cluster), y_total / len(patients_in_same_cluster)]
        patient_num = {}
        for i in range(5):
            patient_num[i] = len(filter(lambda x: x[0] == i, cluster_assement))
        ordered_patient_num = sorted(patient_num.items(), key=operator.itemgetter(1))
        i = 0
        for k, v in ordered_patient_num:
            selectors = [x[0] == k for x in cluster_assement]
            self.hospitals[i].set_coord(self.centers[k][0], self.centers[k][1])
            self.hospitals_patients[self.hospitals[i]] = list(itertools.compress(self.patients, selectors))
            i += 1
        return self.hospitals_patients 

def main():
    kmeans = KMeans("test.txt")
    hospitals_patients = kmeans.k_means() 
    # print hospitals_patients

if __name__ == '__main__':
    main()
