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
    i = 0
    while i < N:
        val = random.randrange(-100,100)
        if val == 0:
            continue
        elif val > 0:
            pos.append(val)
        else:
            neg.append(val)
        i += 1
    pos_sum = sum(pos)
    pos = [float("{0:.2f}".format(x*1.0/pos_sum)) for x in pos]
    pos[-1] += (1-sum(pos))
    print "positive weights sum:",sum(pos)

    _neg_sum = -sum(neg)
    neg = [float("{0:.2f}".format(x*1.0/_neg_sum)) for x in neg]
    neg[-1] -= (sum(neg)+1)
    print "negative weights sum:",sum(neg)
    all = pos + neg
    shuffle(all)
    return all

def random_modify(seq):
    pos_index = [i for i in range(len(seq)) if seq[i] > 0]
    n_change = int(0.05 * len(seq))
    if n_change < 2:
        return seq
    ix1, ix2 = random.sample(pos_index, 2)
    changes = 0.2 * min(seq[ix1], seq[ix2])
    changes = float("{0:.2f}".format(changes))
    print "changes: %s; on weights: %s, %s" % (changes, seq[ix1], seq[ix2])
    seq[ix1] += changes
    seq[ix2] -= changes
    return seq

def modify_candidates():
    num_modify = int(N * 0.05)
    # TODO add modify strategy
    return " ".join(map(str, array))


seq = random_init()
seq_string = " ".join([str(x) for x in seq])
print "Initial weight:",seq_string
while True:
    # res = average_every_value()
    s.sendall(seq_string)
    data = s.recv(8192)
    print "modified weights: ", seq_string 
    if data == "gameover":
        break
s.close()

        
