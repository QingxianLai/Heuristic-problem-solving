import socket
import sys
from random import shuffle
import random

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

def random_init():
    """docstring for random_modify"""
    pos = []
    neg = []
    for i in xrange(N):
        val = random.randrange(-100,100)
        if val >= 0:
            pos.append(val)
        else:
            neg.append(val)
    pos_sum = sum(pos)
    pos = [float("{0:.2f}".format(x*1.0/pos_sum)) for x in pos]
    pos[-1] += (1-sum(pos))
    print "positive weights sum:",sum(pos)

    _neg_sum = -sum(neg)
    neg = [float("{0:.2f}".format(x*1.0/_neg_sum)) for x in neg]
    neg[-1] -= (sum(neg)+1)
    print "negative weights sum:",sum(neg)
    pos.extend(neg)
    shuffle(pos)
    return " ".join([str(x) for x in pos])

def modify_candidates():
    num_modify = int(N * 0.05)
    # TODO add modify strategy
    return " ".join(map(str, array))


rdini = random_init()
print "Initial weight:",rdini
while True:
    # res = average_every_value()
    s.sendall(rdini)
    data = s.recv(8192)
    if data == "gameover":
        break
s.close()

        
