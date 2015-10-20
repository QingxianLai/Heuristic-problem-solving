from KMeans import KMeans
import operator

class Ambulance(object):

    CAPICITY = 4

    def __init__(self, id, hospital):
        """docstring for __init__"""
        self.id = id
        self.hospital = hospital
        self.patients = []
        self.is_full = False
        self.time = 0
        self.x = hospital.x
        self.y = hospital.y

    def pick_up(self, patient, time):
        """docstring for pick_up"""
        self.patients.append(patient)
        self.x = patient.x
        self.y = patient.y
        if len(self.patients)>=self.CAPICITY:
            self.is_full = True
        self.time += time

    def return_to_hospital(self):
        """docstring for return_to_hospital"""

        s = "Ambulance:%s|%s,%s|" % (self.id, self.hospital.x, self.hospital.y)
        for patient in self.patients:
            s += patient.result_print()
            s += ";"
        s = s[:-1]
        s += "|%s,%s" % (self.hospital.x, self.hospital.y)
        print s

        dist = distance(self.x, self.y, self.hospital.x, self.hospital.y)
        self.patients = []
        self.x = self.hospital.x
        self.y = self.hospital.y
        self.time += dist+1
        self.is_full = False


    def time_left(self, current_time):
        min_time = 10000
        for patient in self.patients:
            if min_time > patient.time:
                min_time = patient.time
        return min_time


def distance(x1, y1, x2, y2):
    return abs(x1-x2) + abs(y1-y2)


class RescuePlan(object):
    def __init__(self, hospital, patients, ambu_id_start):
        """docstring for __init__"""
        # print hospital
        # print patients
        self.hospital = hospital
        self.patients = patients
        self.time = 0
        self.save_count = 0
        self.ambulances = []
        ambu_id = ambu_id_start
        for i in xrange(hospital.ambu):
            amb = Ambulance(ambu_id, hospital)
            ambu_id += 1
            hospital.ambu_list.append(amb)
            self.ambulances.append(amb)

    def _find_next_ambulance(self):
        """docstring for find_next"""
        if len(self.ambulances) == 0:
            return None
        latest_ambu = self.ambulances[0]
        latest_time = latest_ambu.time
        for ambu in self.ambulances:
            if latest_time > ambu.time:
                latest_ambu = ambu
                latest_time = ambu.time
        return latest_ambu

    def _time_of_rescue(self, ambulance, patient):
        """docstring for _time_of_rescue"""
        pick_up_time = distance(ambulance.x, ambulance.y, patient.x,
                                      patient.y)
        return_time = distance(patient.x, patient.y, self.hospital.x,
                                     self.hospital.y)
        total_time = pick_up_time + 1 + return_time + 1
        return total_time

    def _find_next_patient(self, ambulance):
        if ambulance.is_full:
            return None
        next_patient = None
        max_time = 0
        for patient in self.patients:
            rescue_time = self._time_of_rescue(ambulance,patient)
            if rescue_time > ambulance.time_left(self.current_time) or rescue_time > patient.time:
                continue
            if max_time< ambulance.time_left(self.current_time) - rescue_time:
                max_time = ambulance.time - rescue_time
                next_patient = patient
        return next_patient

    def _time_elapse(self, seconds):
        for patient in self.patients:
            patient.time -= seconds
            if patient.time <= 0:
                self.patients.remove(patient)

    def plan(self):
        """docstring for plan"""
        self.current_time = 0
        while True:
            if len(self.patients) == 0:
                break
            next_ambu = self._find_next_ambulance()
            if next_ambu is None:
                break
            self._time_elapse(next_ambu.time - self.current_time)
            self.current_time = next_ambu.time
            next_patient = self._find_next_patient(next_ambu)
            if next_patient is None:
                if len(next_ambu.patients) == 0:
                    # TODO: save result here
                    self.ambulances.remove(next_ambu)
                else:
                    self.save_count += next_ambu.patients.__len__()
                    next_ambu.return_to_hospital()
            else:
                time_need = distance(next_ambu.x, next_ambu.y, next_patient.x,
                                     next_patient.y)
                next_ambu.pick_up(next_patient, time_need+1)
                # print "ambu id: %s, patients: %s, is full? %s" % (next_ambu.id, len(next_ambu.patients), next_ambu.is_full)
                # print next_patient
                self.patients.remove(next_patient)
        # print self.save_count
        return self.save_count

def main():
    """docstring for main"""
    kmeans = KMeans("test.txt")
    clusters = kmeans.k_means()
    plan = {}
    saved_num = 0
    ambu_id_start = 1
    plans = []
    sorted_cluster = sorted(clusters.items(), key=lambda x: x[0].id)
    for item in sorted_cluster:
        cluster_plan = RescuePlan(item[0], item[1], ambu_id_start)
        print item[0].result_print()
        ambu_id_start += item[0].ambu
        plans.append(cluster_plan)

    print ""

    for plan in plans:
        num = plan.plan()
        # saved_num += num

    # print "saved %s patients" % saved_num

if __name__ == '__main__':
    main()
