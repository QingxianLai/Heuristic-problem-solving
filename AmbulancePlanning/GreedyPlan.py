from KMeans import *
import sys

class Ambulance(object):
    """docstring for Ambulance"""
    def __init__(self, id, hospital):
        self.id = id
        self.hospital = hospital
        self.patients = []
        self.current_time = 0
        self.x = hospital.x
        self.y = hospital.y
    
class GreedyPlan(object):
    """docstring for GreedyPlan"""
    def __init__(self, file_name):
        self.file_name = file_name
        self.saved_patients = []

    def __savable(self, patient, ambulance, hospital, i):
        return patient.time - self.__distance(patient, ambulance) - ambulance.current_time > (1 + (3 - i) * 0.1) * (self.__distance(patient, hospital) + 1)
    
    def __distance(self, patient, ambulance):
        return abs(patient.x - ambulance.x) + abs(patient.y - ambulance.y)

    def strategy(self):
        kmeans = KMeans(self.file_name)
        hospitals = kmeans.k_means()

        sorted_hospitals = sorted(hospitals.keys())
        k = 1
        for hospital in sorted_hospitals:
            sys.stdout.write("Hospital:" + str(hospital.id) + "|" + str(hospital.x) + "," + str(hospital.y) + "," + str(hospital.ambu) + "|")
            for i in range(hospital.ambu):
                if i != hospital.ambu - 1:
                    sys.stdout.write(str(k) + ",")
                else:
                    sys.stdout.write(str(k) + "\n")
                k += 1
        ambulance_num = k - 1

        k = 1
        print
        for hospital in sorted_hospitals:
            patients = filter(lambda x: x.time >  2.3 * (abs(x.x - hospital.x) + abs(x.y - hospital.y)),hospitals[hospital])
            
            ambu_num = hospital.ambu
            ambulances = []
            for i in range(ambu_num):
                ambulances.append(Ambulance(k, hospital))
                k += 1
            while True:
                pre_num = len(self.saved_patients)
                for i in range(4):
                    for ambulance in ambulances:
                        patients = sorted(patients, key=lambda x: abs(x.x - ambulance.x) + abs(x.y - ambulance.y))
                        for patient in patients:
                            if self.__savable(patient, ambulance, hospital, i):
                                ambulance.patients.append(patient)
                                patients.remove(patient)
                                ambulance.current_time += self.__distance(patient, ambulance) + 1
                                ambulance.x = patient.x
                                ambulance.y = patient.y
                                break
                for ambulance in ambulances:
                    if len(ambulance.patients) == 0:
                        continue
                    sys.stdout.write("Ambulance:" + str(ambulance.id) + "|" + str(hospital.x) + "," + str(hospital.y) + "|")
                    ambulance.current_time += self.__distance(ambulance, hospital) + 1
                    first = True
                    for patient in ambulance.patients:
                        
                        if patient.time >= ambulance.current_time:
                            if first:
                                sys.stdout.write(str(patient.id) + "," + str(patient.x) + "," + str(patient.y) + "," + str(patient.time))
                                first = False
                            else:
                                sys.stdout.write(";" + str(patient.id) + "," + str(patient.x) + "," + str(patient.y) + "," + str(patient.time))
                            self.saved_patients.append(patient)
                    sys.stdout.write("|" + str(hospital.x) + "," + str(hospital.y) + "\n")
                    ambulance.patients = []
                    ambulance.x = hospital.x
                    ambulance.y = hospital.y
                if len(self.saved_patients) == pre_num:
                    break
        print len(self.saved_patients) 

def main():
    plan = GreedyPlan(sys.argv[1])
    plan.strategy()

if __name__ == '__main__':
    main()
