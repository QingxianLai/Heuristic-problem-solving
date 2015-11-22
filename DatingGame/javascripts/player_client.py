import socket
import sys
from random import shuffle

HOST = '127.0.0.1'
PORT = 6969
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
s.connect((HOST,PORT)) 

N = int(sys.argv[1])
first = True

array = []

def average_every_value():
    res = []
    if N % 2 == 1:
        res.append(0)
    avg = float("{0:.4f}".format(1.0 / (N / 2)))
    for i in range(N / 2 - 1):
        res.append(avg)
        res.append(-avg)
    res.append(1 - avg * (N / 2 - 1))
    res.append(-1 + avg * (N / 2 - 1))
    shuffle(res)
    array = res
    return " ".join(map(str, res))

def modify_candidates():
    num_modify = int(N * 0.05)
    # TODO add modify strategy
    return " ".join(map(str, array))

while True:
    res = average_every_value()
    s.sendall(res)
    data = s.recv(8192)
    if data == "gameover":
        break
s.close()
