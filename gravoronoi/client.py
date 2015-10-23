import sys
import random
import time

from twisted.internet import reactor, protocol

board_size = 1000

class Client(protocol.Protocol):
    """Random Client"""
    def __init__(self, name):
        self.name = name
        self.prev_moves = []

    def make_random_move(self):
        move = None
        while not move:
            x = random.randint(0, board_size-1)
            y = random.randint(0, board_size-1)
            if (x, y) not in self.prev_moves:
                move = (x, y)
        return move

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
