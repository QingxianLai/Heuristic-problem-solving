import socket
import re
from sklearn.linear_model import Ridge

HOST = '127.0.0.1'
PORT = 9696
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
s.connect((HOST,PORT)) 

total_data = []

def split_data(data):
    data = data.split("\n")[:-1]
    data_set = map(lambda x: re.split("[| ]", x.strip()), data)
    res = []
    for item in data_set:
        item = map(lambda x: float("{0:.4f}".format(float(x))), filter(lambda x: x != '', item))
        res.append(item)
    return res

while True:
    data=s.recv(65536)
    if data == "gameover":
        break
    data_split = split_data(data)
    total_data.extend(data_split)
    x_train = map(lambda x: x[:-1], total_data)
    y_train = map(lambda x: x[-1], total_data)
    regr = Ridge()
    regr.fit(x_train, y_train)
    res = reduce(lambda x, y: x + "1 " if y > 0 else x + "0 ", regr.coef_, "")
    s.sendall(res[:-1])
s.close()
