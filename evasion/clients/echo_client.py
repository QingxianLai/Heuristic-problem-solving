import websocket
import sys
import json

class GameStrategy(object):
    def __init__(self, role, ws):
        """docstring for __init__"""
        self.role = role
        self.ws = ws

    def _send_to_server(self, json_command):


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
    print "%s, Welcome!" % role

    while True:
        a = raw_input("command >")
        pack = {}
        if a == "B":
            wall_length = raw_input("wall_lenth >")
            wall_direct = raw_input("wall direction >")
            pack = {"command": "B", "wall": {"length": wall_length,
                                             "direction": wall_direct}}
        elif a == "D":
            wall_index = raw_input("wall index>")
            pack = {"command": "D", "wallindex": wall_index}
        elif a == "M":
            if role == "P":
                direction = raw_input("move direction>")
                pack = {"command": "M", "direction": direction}
            else:
                pack = {"command": "M"}
        elif a == "P":
            pack = {"command": "P"}
        elif a == "W":
            pack = {"command": "W"}
        else:
            print "unknown command"
            continue
        json_string = json.dumps(pack)
        print "==|| message sent: %s" % json_string
        ws.send(json_string)
        result = ws.recv()
        print "==|| Get message: %s" % result

if __name__ == '__main__':
    main()
