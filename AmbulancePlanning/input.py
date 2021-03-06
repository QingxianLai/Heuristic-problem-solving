

class Patient(object):
    def __init__(self, no, x, y, time):
        """docstring for __init__"""
        self.id = no
        self.x = x
        self.y = y
        self.time = time
        self.origin_time = time

    def result_print(self):
        output = "%s,%s,%s,%s" % (self.id, self.x, self.y, self.origin_time)
        return output

    def __repr__(self):
        return "patient: " + str(self.id) + ", x: " + str(self.x) + " y: " + str(self.y) + " time: " + str(self.time)


class Hospital(object):
    def __init__(self, id, num_ambulance):
        """docstring for __init__"""
        self.id = id
        self.ambu = num_ambulance
        self.x = -1
        self.y = -1
        self.ambu_list = []

    def add_ambulance(self, ambu):
        """docstring for add_ambulance"""
        self.ambu_list.add(ambu);

    def set_coord(self, x, y):
        """docstring for set_coord"""
        self.x = x
        self.y = y

    def result_print(self):
        """docstring for result_print"""
        output = "Hospital:%s|%s,%s,%s|" % (self.id, self.x, self.y, self.ambu)
        for ambu in self.ambu_list:
            output = output + str(ambu.id) + ","
        output = output[:-1]
        return output


    def __repr__(self):
        return "Hospital: " + str(self.id) + " x: " + str(self.x) + " y: " + str(self.y)


def read_from_file(path, num_patients=300, num_hospitals=5):
    """
    return list of Patient object and list of Hospital object
    """
    f = open(path, 'rb')

    patients = []
    hospitals = []

    # read patients
    f.readline() # read the headline of patients
    for i in xrange(num_patients):
        ss = f.readline()
        tmp = [int(x) for x in ss.split(",")]
        patient = Patient(i+1, tmp[0], tmp[1], tmp[2])
        patients.append(patient)

    # read hospitals
    f.readline() # read in the space line
    f.readline() # read the headline of hospitals
    for i in xrange(num_hospitals):
        ss = f.readline()
        tmp = int(ss)
        hospital = Hospital(i+1, tmp)
        hospitals.append(hospital)

    f.close()
    return patients, hospitals


def test():
    """docstring for test"""
    patients, hospitals = read_from_file("test.txt")
    print len(patients)
    print len(hospitals)


if __name__ == '__main__':
    test()
