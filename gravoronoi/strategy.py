import sys
import random
import time
import math

from twisted.internet import reactor, protocol

board_size = 1000

class Client(protocol.Protocol):
    def __init__(self, name):
        self.name = name
        self.prev_moves = []
        self.my_moves = []

    def calculate_distance(self):
        opponent = 0
        mine = 0
        for i in range(85, board_size - 85):
            for j in range(85, board_size - 85):
                oppo_pull = 0
                for move in self.prev_moves:
                    dist = (i - move[0]) ** 2 + (j - move[1]) ** 2
                    if dist == 0:
                        continue
                    oppo_pull += 1.0 / dist
                my_poll = 0
                #print "my_moves:", self.my_moves
                for move in self.my_moves:
                    dist = (i - move[0]) ** 2 + (j - move[1]) ** 2
                    if dist == 0:
                        continue
                    my_poll += 1.0 / dist
                if oppo_pull > my_poll:
                    opponent += 1
                else:
                    mine += 1
        return mine - opponent

    def make_random_move(self):
        if self.prev_moves != []:
            return self.second_move()
        else:
            return self.first_move()

    def first_move(self):
        return (0, 0)

    def second_move(self):
        max = 0
        best_move = ()
        move = self.prev_moves[-1]
        if move[0] - 1 >= 0:
            if (move[0] - 1, move[1]) not in self.prev_moves and (move[0] - 1, move[1]) not in self.my_moves:
                self.my_moves.append((move[0] - 1, move[1]))
                cur = self.calculate_distance()
                if cur > max:
                    max = cur
                    best_move = (move[0] - 1, move[1])
                del self.my_moves[-1]
        if move[0] + 1 <= 999:
            if (move[0] + 1, move[1]) not in self.prev_moves and (move[0] + 1, move[1]) not in self.my_moves:
                self.my_moves.append((move[0] + 1, move[1]))
                cur = self.calculate_distance()
                if cur > max:
                    max = cur
                    best_move = (move[0] + 1, move[1])
                del self.my_moves[-1]
        if move[1] - 1 >= 0:
            if (move[0], move[1] - 1) not in self.prev_moves and (move[0], move[1] - 1) not in self.my_moves:
                self.my_moves.append((move[0], move[1] - 1))
                cur = self.calculate_distance()
                if cur > max:
                    max = cur
                    best_move = (move[0], move[1] - 1)
                del self.my_moves[-1]
        if move[1] + 1 <= 999:
            if (move[0], move[1] + 1) not in self.prev_moves and (move[0], move[1] + 1) not in self.my_moves:
                self.my_moves.append((move[0], move[1] + 1))
                cur = self.calculate_distance()
                if cur > max:
                    max = cur
                    best_move = (move[0], move[1] + 1)
                del self.my_moves[-1]
        print best_move, max
        return best_move

    def dataReceived(self, data):
        print "Received: %r" % data
        line = data.strip()
        items = line.split("\n")
        if items[-1] == "TEAM":
            self.transport.write(self.name)
        elif items[-1] == "MOVE":
            for item in items[:-1]:
                parts = item.split()
                player, x, y = parts[0], int(parts[1]), int(parts[2])
                # make a random move
                self.prev_moves.append((x, y))
            move = self.make_random_move()
            self.my_moves.append(move)
            print "making move %r" % str(move)
            self.transport.write("{0} {1}".format(move[0], move[1]))
        elif items[-1] == "END":
            self.transport.loseConnection()

    def connectionLost(self, reason):
        reactor.stop()

class ClientFactory(protocol.ClientFactory):
    """ClientFactory"""
    def __init__(self, name):
        self.name = name

    def buildProtocol(self, addr):
        c = Client(self.name)
        c.addr = addr
        return c

    def clientConnectionFailed(self, connector, reason):
        print "Connection failed - goodbye!"
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print "Connection lost - goodbye!"

def main():
    if len(sys.argv) != 2:
        print "provide arg for client name"
        sys.exit()
    client_name = sys.argv[1]
    factory = ClientFactory(client_name)
    reactor.connectTCP("127.0.0.1", 1337, factory)
    reactor.run()


if __name__ == '__main__':
    main()
