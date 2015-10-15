from KMeans import *

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
        return patient.time - self.__distance(patient, ambulance) > (1 + (4 - i) * 0.1) * self.__distance(patient, hospital)
    
    def __distance(self, patient, ambulance):
        return abs(patient.x - ambulance.x) + abs(patient.y - ambulance.y)

    def strategy(self):
        kmeans = KMeans(self.file_name)
        hospitals = kmeans.k_means()
        j = 1
        for hospital in hospitals:
            patients = filter(lambda x: x.time >  2.3 * (abs(x.x - hospital.x) + abs(x.y - hospital.y)),hospitals[hospital])
            
            ambu_num = hospital.ambu
            ambulances = []
            for i in range(ambu_num):
                ambulances.append(Ambulance(i, hospital))
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
                    ambulance.current_time += self.__distance(ambulance, hospital) + 1
                    for patient in ambulance.patients:
                        if patient.time >= ambulance.current_time:
                            self.saved_patients.append(patient)
                    ambulance.patients = []
                    ambulance.x = hospital.x
                    ambulance.y = hospital.y
                if len(self.saved_patients) == pre_num:
                    break

def main():
    plan = GreedyPlan("test.txt")
    plan.strategy()
    print plan.saved_patients
    print len(plan.saved_patients)

if __name__ == '__main__':
    main()
