import socket
import random

HOST = '127.0.0.1'
PORT = 6969
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
s.connect((HOST,PORT)) 

#test
while True:
    res = "0.3 -0.3 0.2 -0.2 0.4 -0.4 0.05 -0.05 0.05 -0.05"
    for i in range(10):
        res += " 0"
    s.sendall(res)
    data = s.recv(1024)
    print data
    if data == "continue":
        s.sendall(res)
    if data == "gameover":
        break
s.close()
