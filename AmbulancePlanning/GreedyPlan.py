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
        self.ambulance_patients = {}

    def __savable(self, patient, ambulance, hospital, i):
        return patient.time - self.__distance(patient, ambulance) - ambulance.current_time > (1 + (4 - i) * 0.1) * self.__distance(patient, hospital)
    
    def __distance(self, patient, ambulance):
        return abs(patient.x - ambulance.x) + abs(patient.y - ambulance.y)

    def strategy(self):
        kmeans = KMeans(self.file_name)
        hospitals = kmeans.k_means()
        f = open("result.txt", "w")

        sorted_hospitals = sorted(hospitals.keys())
        k = 1
        for hospital in sorted_hospitals:
            f.write("Hospital:" + str(hospital.id) + "|" + str(hospital.x) + "," + str(hospital.y) + "," + str(hospital.ambu) + "|")
            for i in range(hospital.ambu):
                if i != hospital.ambu - 1:
                    f.write(str(k) + ",")
                else:
                    f.write(str(k) + "\n")
                k += 1
        ambulance_num = k - 1

        k = 1
        f.write("\n")
        ambulance_id = {}
        for hospital in sorted_hospitals:
            patients = filter(lambda x: x.time >  2.3 * (abs(x.x - hospital.x) + abs(x.y - hospital.y)),hospitals[hospital])
            
            ambu_num = hospital.ambu
            ambulances = []
            for i in range(ambu_num):
                ambulances.append(Ambulance(k, hospital))
                ambulance_id[ambulances[-1].id] = ambulances[-1]
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
                    ambulance.current_time += self.__distance(ambulance, hospital) + 1
                    for patient in ambulance.patients:
                        if patient.time >= ambulance.current_time:
                            if ambulance.id not in self.ambulance_patients:
                                self.ambulance_patients[ambulance.id] = []
                                self.ambulance_patients[ambulance.id].append(patient)
                            else:
                                self.ambulance_patients[ambulance.id].append(patient)
                            self.saved_patients.append(patient)
                    ambulance.patients = []
                    ambulance.x = hospital.x
                    ambulance.y = hospital.y
                if len(self.saved_patients) == pre_num:
                    break
        for id in range(1, ambulance_num + 1):
            f.write("Ambulance:" + str(id) + "|" + str(ambulance_id[id].x) + "," + str(ambulance_id[id].y) + "|")
            for i in range(len(self.ambulance_patients[id])):
                patient = self.ambulance_patients[id][i]
                if i != len(self.ambulance_patients[id]) - 1:
                    f.write(str(patient.id) + "," + str(patient.x) + "," + str(patient.y) + "," + str(patient.time) + ";")
                else:
                    f.write(str(patient.id) + "," + str(patient.x) + "," + str(patient.y) + "," + str(patient.time) + "|" + str(ambulance_id[id].x) + "," + str(ambulance_id[id].y) + "\n")
        f.close()


def main():
    plan = GreedyPlan("test.txt")
    plan.strategy()

if __name__ == '__main__':
    main()
