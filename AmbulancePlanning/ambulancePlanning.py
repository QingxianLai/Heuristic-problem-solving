import input
from input import Hospital, Patient

class Ambulance(object):

    CAPICITY = 4

    def __init__(self, id, hospital):
        """docstring for __init__"""
        self.id = id
        self.hospital = hospital
        self.patients = []
        self.time = 0
        self.time_left = 100000
        self.is_full = False

    def pick_up(self, patient):
        """docstring for pick_up"""
        self.patients.append(patient)
        self.time_left = min(patient.time, self.time_left)
        if len(self.patients)==CAPICITY:
            self.is_full == True


class rescue_plan(object):
    def __init__(self, hospital, patients):
        """docstring for __init__"""
        self.hospital = hospital
        self.patients = patients
        self.time = 0
        self.ambulances = []
        for i in xrange(hospital.ambu):
            amb = Ambulance(i+1, hospital)
            self.ambulances.append(amb)

    def _find_next(self):
        """docstring for find_next"""


def rescue_plan(hospital, patients):
    time = 0
    ambulances = []
    for i in xrange(hospital.ambu):
        amb = Ambulance(i+1, hospital)
        ambulances.append(amb)

    next_time, next_ambulance = find_next(ambulances)


def find_next(ambulances):
    """docstring for find_next"""
    latest_ambu = ambulances[0]
    latest_time = latest_ambu.time
    for ambu in ambulances:
        if latest_time > ambu.time:
            latest_ambu = ambu
            latest_time = ambu.time
    return latest_ambu, latest_time



def main():
    """docstring for main"""
    patients, hospitals = input.read_from_file("test.txt")


if __name__ == '__main__':
    main()
