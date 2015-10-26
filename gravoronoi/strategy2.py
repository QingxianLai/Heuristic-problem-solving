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
        if len(self.my_moves) >=  len(self.prev_moves):
            return self.player1_move()
        else:
            return self.player2_move()

    def _find_majority(self, coord1, coord2):
        """docstring for _find_majority"""
        if coord1[0] > coord2[0]:
            return self._find_majority(coord2, coord1)
        our_stones = [x for x in self.my_moves if x[0]>coord1[0] and x[0] < coord2[0] and x[1] > coord1[1] and x[1] < coord2[1]]
        ops_stones = [x for x in self.prev_moves if x[0]>coord1[0] and x[0] < coord2[0] and x[1] > coord1[1] and x[1] < coord2[1]]
        if len(our_stones) != len(ops_stones):
            return  len(our_stones) > len(ops_stones)
        own = 0
        ops = 0
        for i in range(coord1[0], coord2[0]):
            for j in range(coord1[1], coord2[1]):
                if (i,j) in set(our_stones + ops_stones):
                    continue
                our_pull = 0.0
                for stone in our_stones:
                    our_pull += 1.0/ ((i - stone[0])**2 + (j-stone[1])**2)

                ops_pull = 0.0
                for stone in ops_stones:
                    ops_pull += 1.0/ ((i - stone[0])**2 + (j-stone[1])**2)

                if our_pull > ops_pull:
                    own += 1
                else:
                    ops += 1
        # print "======> area (%s, %s) to (%s, %s) has own stone %s, ops stone %s, has own color: %s, and opposit color %s" % (coord1[0], coord1[1],
                                                            # coord2[0], coord2[1],
                                                            # len(our_stones),
                                                            # len(ops_stones),
                                                            # own, ops)
        return own > ops

    def _opposite_move(self, last_move):
        """docstring for _opposite_move"""
        new_x = 0
        new_y = 0
        if last_move[0] < board_size/2:
            new_x = last_move[0]-15
        else:
            new_x = last_move[0]+15

        if last_move[1] < board_size/2:
            new_y = last_move[1]-15
        else:
            new_y = last_move[1]+15
        return (new_x, new_y)


    def _go_pos_move(self, last_move):
        """docstring for _go_pos_move"""
         # left up corner
        if not self._find_majority((0,0),(180,180)):
            return self._find_edge_pos((180,180))

         # right up corner
        if not self._find_majority((820,0),(999,180)):
            return self._find_edge_pos((820,180))

        # left down corner
        if not self._find_majority((0,820),(180,999)):
            return self._find_edge_pos((180,820))

        # right down corner
        if not self._find_majority((820,820),(999,999)):
            return self._find_edge_pos((820,820))

        # up mid
        if not self._find_majority((350,0),(650,180)):
            return self._find_edge_pos((500,180))

        # down mid
        if not self._find_majority((350,820),(650,999)):
            return self._find_edge_pos((500,820))

        # left mid
        if not self._find_majority((0,350),(180,650)):
            return self._find_edge_pos((180,500))

        # right mid
        if not self._find_majority((820,350),(820,650)):
            return self._find_edge_pos((820,500))

        return self._find_edge_pos(last_move)

    def _find_edge_pos(self, last_move):
        """docstring for _find_edge_pos"""
        close_to_left = True
        close_to_up = True
        x = last_move[0]
        y = last_move[1]
        if x >= board_size/2:
            close_to_left = False
        if y >= board_size/2:
            close_to_up = False
        new_x = x;
        new_y = y;
        pos_dis = 1
        corner_thresh = 40
        if close_to_left:
            if close_to_up:
                # TODO: corner case when point on the edge
                if abs(new_x - new_y) <= corner_thresh:
                    new_x -= pos_dis
                    new_y -= pos_dis
                elif new_x > new_y:
                    new_y -= pos_dis
                elif new_x < new_y:
                    new_x -= pos_dis
            else:
                # TODO corner case
                if abs(new_x - (1000 - new_y)) <= corner_thresh:
                    new_x -= pos_dis
                    new_y += pos_dis
                elif new_x > 1000 - new_y:
                    new_y += pos_dis
                elif new_x < 1000 - new_y:
                    new_x -= pos_dis
        else:
            if close_to_up:
                # TODO: corner case when point on the edge
                if abs(1000 - new_x - new_y) <= corner_thresh:
                    new_x += pos_dis
                    new_y -= pos_dis
                elif 1000 - new_x > new_y:
                    new_y -= pos_dis
                elif 1000 - new_x < new_y:
                    new_x += pos_dis
            else:
                # TODO corner case
                if abs(1000 - new_x - (1000 - new_y)) <= corner_thresh:
                    new_x += pos_dis
                    new_y += pos_dis
                elif new_x > 1000 - new_y:
                    new_y += pos_dis
                elif new_x < 1000 - new_y:
                    new_x += pos_dis

        if self._verify_posi(new_x,new_y):
            return (new_x, new_y)
        else:
            return self._find_edge_pos((new_x, new_y))

    def _verify_posi(self, x, y):
        """docstring for _verify_pos"""
        if x<0 or x>=board_size or y < 0 or y > board_size:
            return False
        all_stones = self.prev_moves + self.my_moves
        for coord in all_stones:
            if x == coord[0] and y == coord[1]:
                return False
        return True

    def player1_move(self):
        print self.my_moves, "1111111111111111111"
        if self.my_moves == []:
            return (499, 499)
        else:
            last_move = self.prev_moves[-1];
            next_move = self._go_pos_move(last_move)
            return next_move


    def player2_move(self):
        """docstring for player2_move"""
        # time.sleep(2)
        last_move = self.prev_moves[-1];
        next_move = self._go_pos_move(last_move)
        return next_move

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
            move = self.player2_move()
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
