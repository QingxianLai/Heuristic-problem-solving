import websocket
import sys
import json


class GameStrategy(object):
    def __init__(self, role, ws, publisher):
        """docstring for __init__"""
        self.role = role
        self.ws = ws
        self.publisher = publisher
        self.first_move = True

    def _send_to_server(self, command_dict):
        """docstring for _send_to_server"""
        json_string = json.dumps(command_dict)
        self.ws.send(json_string)
        return_msg = None
        if command_dict['command'] == "P" or command_dict['command'] == "W":
            return_msg = self.ws.recv()
        return return_msg

    def hunterStrategy(self):
        """docstring for hunterStrategy"""
        while self.ws.connected:
            if self.first_move:
                self._send_to_server({"command": "M"})
                self.first_move = False
            else:
                while self.publisher.recv():
                    self._send_moving_message()
                    a = self._get_position()
                    print a


    def prey_strategy(self):
        """docstring for preyStrategy"""
        while self.ws.connected:
            if self.first_move:
                self._send_moving_message("N")
                self.first_move = False
            else:
                while self.publisher.recv():
                    self._send_moving_message("S")
                    a = self._get_position()
                    print a
                    
    def _get_direction(self, pos1, pos2):
        if pos1[0] == pos2[0] and pos1[1] < pos2[1]:
            return "S"
        elif pos1[0] == pos2[0] and pos1[1] > pos2[1]:
            return "N"
        elif pos1[0] < pos2[0] and pos1[1] == pos2[1]:
            return "E"
        elif pos1[0] > pos2[0] and pos1[1] == pos2[1]:
            return "W"
        elif pos1[0] > pos2[0] and pos1[1] > pos2[1]:
            return "NW"
        elif pos1[0] < pos2[0] and pos1[1] > pos2[1]:
            return "NE"
        elif pos1[0] < pos2[0] and pos1[1] < pos2[1]:
            return "SE"
        elif pos1[0] > pos2[0] and pos1[1] < pos2[1]:
            return "SW"

    def _send_moving_message(self, direction=""):
        if direction == "":
            message = {"command": "M"}
        else:
            message = {"command": "M", "direction": direction}
        self._send_to_server(message)
    
    def _get_walls(self):
        message = {"command": "W"}
        json_string = self._send_to_server(message)
        obj = json.loads(json_string)
        walls = obj["walls"]
        return walls

    def _get_position(self):
        message = {"command": "P"}
        json_string = self._send_to_server(message)
        obj = json.loads(json_string)
        return obj

    def run(self):
        """docstring for run"""
        if self.role == "H":
            self.hunterStrategy()
        else:
            self.prey_strategy()


def main():
    """docstring for main"""
    publisher = websocket.create_connection("ws://localhost:1990")
    if sys.argv[1] == "H":
        role = "H"
        port = "1991"
        url = "ws://localhost:" + port
        ws = websocket.create_connection(url)
        # prey = websocket.create_connection("ws://localhost:1992")
    else:
        role = 'P'
        port = "1992"
        url = "ws://localhost:" + port
        ws = websocket.create_connection(url)
        # hunter = websocket.create_connection("ws://localhost:1991")
    strategy = GameStrategy(role, ws, publisher)
    strategy.run()

if __name__ == '__main__':
    main()
