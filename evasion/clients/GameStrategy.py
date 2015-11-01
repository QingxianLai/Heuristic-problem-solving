import websocket
import sys
import json

class GameStrategy(object):
    def __init__(self, role, ws):
        """docstring for __init__"""
        self.role = role
        self.ws = ws

    def _send_to_server(self, command_dict):
        """docstring for _send_to_server"""
        json_string = json.dumps(command_dict)
        self.ws.send(json_string)
        return_msg = None
        if command_dict['command'] == "P" or command_dict['command']=="W":
            return_msg = self.ws.recv()
        return return_msg

    def hunterStrategy(self):
        """docstring for hunterStrategy"""
        pass

    def preyStrategy(self):
        """docstring for preyStrategy"""
        pass

    def run(self):
        """docstring for run"""
        if self.role == "H":
            self.hunterStrategy()
        else:
            self.preyStrategy()


def main():
    """docstring for main"""
    role = "H"
    port = "1991"
    if len(sys.argv) > 1:
        role = sys.argv[1]
        if role == 'P':
            port = "1992"
    url = "ws://localhost:" + port
    ws = websocket.create_connection(url)
    strategy = GameStrategy(role, ws)
    strategy.run()

if __name__ == '__main__':
    main()

