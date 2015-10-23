from twisted.internet import protocol
import datetime

board_size = 1000

class GameServer(protocol.Protocol):

    def __init__(self, window, manager):
        self.window = window
        self.manager = manager
        self.players = manager["players"]
        self.state = "GETNAME"
        self.name = None

    def dataReceived(self, data):
        # stop the timer
        line = data.strip()
        print "Received: %r" % line
        if self.state == "GETNAME":
            self.handle_getname(line)
        elif self.state == "PLAYING":
            cur_time = datetime.datetime.now()
            self.manager["times"][self.name] += cur_time - self.factory.start_time
            items = line.split()
            if len(items) == 2:
                try:
                    move = (int(items[0]), int(items[1]))
                    self.handle_move(move)
                except Exception as e:
                    self.transport.write(str(e))
            else:
                self.transport.write("Error: Invalid number of move parameters.")
        elif self.state == "END":
            self.transport.write("GAME ENDED")

    def handle_getname(self, name):
        if self.players.get(name):
            self.transport.write("Error: team name taken, try again.")
        else:
            # names must be lower case
            self.name = name.lower()
            self.players[self.name] = self
            self.state = "PLAYING"
            print self.players.keys()
            # Check if all the players are connected, start game if so
            if len(self.players) == self.factory.num_players:
                print "All players connected, start game!"
                self.factory.call_next_player()

    def validate_move(self, player_id, move, move_num):
        if self.manager["current_protocol"] != self:
            return False
        x, y = move
        if x < 0 or x > board_size - 1 or y < 0 or y > board_size - 1:
            return False
        points = self.window.points
        for player_id in self.manager["player_ids"].values():
            for move_num in range(self.manager["move_num"]+1):
                if points[player_id, move_num, 0] == x and points[player_id, move_num, 1] == y:
                    return False
        return True

    def handle_move(self, move):
        player_id = self.manager["player_ids"][self.name]
        move_num = self.manager["move_num"]
        if not self.validate_move(player_id, move, move_num):
            print "Invalid move detected"
            self.transport.write("INVALID MOVE")
            return
        print "%r making move: move=%r move_num=%r" % (self.name, move, move_num)
        self.window.updateUI(player_id, move, move_num)
        if len(self.manager["move_buffer"]) == self.factory.num_players - 1:
            self.manager["move_buffer"].pop(0)
        self.manager["move_buffer"].append((self.name, move[0], move[1]))
        self.factory.call_next_player()

    def connectionMade(self):
        print "Connected with client %r" % self.addr
        self.manager["num_connected"] += 1
        self.transport.write("TEAM")
        print "Number of connected players %r" % self.manager["num_connected"]

    def connectionLost(self, reason):
        self.manager["num_connected"] -= 1
        if self.name and self.players.get(self.name):
            del self.players[self.name]
        print "Connection lost with client %r, reason %r" % (self.addr, reason)


class GameServerFactory(protocol.ServerFactory):

    protocol = GameServer

    def __init__(self, window, start_player, num_players=2, num_moves=10, gui_on=1):
        self.window = window
        # Manager is a global object shared by all clients
        self.manager = {
            "num_connected": 0,
            "players": {},  # Map from player name to GameServer protocol
            "player_ids": {}, # Map from player name to their id (0 to n-1)
            "current_protocol": None,
            "move_num": 0,
            "move_buffer": [],
            "times": {}
        }
        self.num_moves = num_moves
        self.num_players = num_players
        self.start_player = start_player
        self.player_gen = None
        self.start_time = None
        self.gui_on = gui_on

    def reset(self):
        self.manager = {
            "num_connected": 0,
            "players": {},  # Map from player name to GameServer protocol
            "player_ids": {}, # Map from player name to their id (0 to n-1)
            "current_protocol": None,
            "move_num": 0,
            "move_buffer": [],
            "times": {}
        }
        self.player_gen = None
        self.start_time = None

    def next_player_generator(self):
        "Generate the next player protocol by round robin"
        protocols = []
        id_counter = 0
        # some state initialization here
        for team_name, protocol in self.manager["players"].iteritems():
            self.manager["player_ids"][team_name] = id_counter
            self.manager["times"][team_name] = datetime.timedelta(0)
            protocols.append((team_name, protocol))
            self.window.addPlayerName(team_name)
            id_counter += 1
        i = self.manager["player_ids"].get(self.start_player, 0)
        turn_counter = 0
        while 1:
            yield protocols[i]
            i = (i + 1) % self.num_players
            turn_counter += 1
            # increase move num if all players made a move
            if turn_counter == self.num_players:
                turn_counter = 0
                self.manager["move_num"] += 1

    def call_next_player(self):
        if not self.player_gen:
            self.player_gen = self.next_player_generator()
        team_name, protocol = self.player_gen.next()
        if self.manager["move_num"] < self.num_moves:
            self.manager["current_protocol"] = protocol
            # return previous num_player moves, this is signal for player to make move
            prev_moves = ["{0} {1} {2}".format(move[0], move[1], move[2]) for move in self.manager["move_buffer"]]
            s = "\n".join(prev_moves + ["MOVE"])
            protocol.transport.write(s)
            # start timer here
            self.start_time = datetime.datetime.now()
        else:
            print "Game ended"
            # Notify players game has ended
            for t, p in self.manager["players"].iteritems():
                p.state = "END"
                p.transport.write("END")
            print "\n==========\nPlay Times\n=========="
            for team_name, time in self.manager["times"].iteritems():
                print "{0}: {1}".format(team_name, str(time))
            # Print the scores
            print "\n======\nScores\n======"
            scores = self.window.endMatch()
            for team_name, pid in self.manager["player_ids"].iteritems():
                print "{0}: {1}".format(team_name, scores[pid])
            print
            self.reset()
            if not self.gui_on:
                self.window.close()

    def buildProtocol(self, addr):
        gs = GameServer(self.window, self.manager)
        gs.addr = addr
        gs.factory = self
        return gs
